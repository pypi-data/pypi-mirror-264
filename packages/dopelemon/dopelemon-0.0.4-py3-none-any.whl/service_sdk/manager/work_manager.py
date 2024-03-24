from logging import getLogger, Logger
from time import sleep, time
from typing import Optional, Callable, Any

from service_sdk.exceptions import TimeoutWaitingForWorkerToStop
from service_sdk.manager.controller import Controller
from service_sdk.manager.registry import Registry
from service_sdk.worker.worker import Worker


class WorkManager:
    def __init__(
            self,
            name=None,
            logger: Optional[Logger] = None,
            work_callback: Optional[Callable[[Any], Any]] = None,
            max_workers: int = 2,
    ):
        self.name = name
        self.logger = logger or getLogger(__name__)
        self.work_callback = work_callback or (lambda **_: None)
        self.max_workers = max_workers
        self._registry = Registry(max_workers=max_workers)

    def start_worker(self, **kwargs):
        self._update_workers_status()
        self.logger.info("Starting worker")

        if self._registry.counter >= self.max_workers:
            self.logger.info("Max worker capacity reached.")
            return

        worker = Worker(controller=Controller(), work_callback=self.work_callback)
        self._registry.add(worker=worker)
        worker.start()
        self.logger.info(f"Worker started. uid={worker.uid}, pid={worker.get_pid()}.")

    def stop_all(self, wait: bool = True, timeout: int = 10):
        for worker in self._registry.all():
            worker.controller.set_stop()

        if wait:
            self._wait_for_workers_to_stop(timeout=timeout)

    def stop_by_uid(self, uid: str) -> Optional[str]:
        worker = self._registry.get(id_=uid)
        if not worker:
            return
        worker.controller.set_stop()
        self._update_workers_status()
        return worker.uid

    def kill_all(self, wait: bool = True, timeout: int = 10):
        for worker in self._registry.all():
            worker.process.kill()

        if wait:
            self._wait_for_workers_to_stop(timeout=timeout)

    def _wait_for_workers_to_stop(self, timeout: int = 10):
        start_time = time()
        while self._registry.counter > 0:
            if time() - start_time > timeout:
                self.logger.error(
                    f"Reached {timeout=} while waiting for workers to stop. {self._registry.counter} left."
                )
                raise TimeoutWaitingForWorkerToStop()

            self._update_workers_status()
            self.logger.info(f"Waiting for workers to stop. {self._registry.counter} left.")
            sleep(0.5)

    def get_status(self):
        self._update_workers_status()
        status = {}
        for worker in self._registry.all():
            status[worker.uid] = worker.controller.get_status()
        return status

    def restart(self):
        self.stop_all()
        self.start_worker()

    def _update_workers_status(self):
        for worker in self._registry.all():
            if not worker.process.is_alive():
                self._registry.remove(id_=worker.uid)
