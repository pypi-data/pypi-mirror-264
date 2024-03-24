import sys
import threading
import ctypes


class ExThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def run(self):
        # target function of the thread class
        try:
            super().run()
        except BaseException as exception:
            print(f"Thread {self.get_id()} got {exception=}")
            print(sys.exc_info())

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id_, thread in threading._active.items():
            if thread is self:
                return id_

    def raise_exception(self, exception):
        if not issubclass(exception, Exception):
            raise ValueError(f"Not a valid exception <{type(exception)}>.")

        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(exception)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
