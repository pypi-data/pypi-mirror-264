from typing import Optional

from service_sdk.worker.worker import Worker


class Registry:
    def __init__(self, max_workers: int = 1):
        self._max_workers = max_workers
        self._workers_count = 0
        self._registry = {}

    @property
    def max(self):
        return self._max_workers

    @property
    def counter(self):
        return self._workers_count

    def add(self, worker: Worker):
        self._registry[worker.uid] = worker
        self._workers_count += 1

    def remove(self, id_: str):
        del self._registry[id_]
        self._workers_count -= 1

    def all(self):
        return list(self._registry.values())

    def get(self, id_: str) -> Optional[Worker]:
        return self._registry.get(id_)
