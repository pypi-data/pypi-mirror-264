from copy import copy
from multiprocessing import Lock, Value, Queue
from ctypes import c_int, c_bool


class Controller:
    default_timeout_sec = 10

    def __init__(self):
        self._lock: Lock = Lock()
        self._stop_flag = Value(c_bool, False)
        self._status = Value(c_int, 0)
        self._input = Queue()
        self._output = Queue()

    def set_stop(self, value: bool = True):
        with self._lock:
            self._stop_flag.value = value

    def get_stop(self):
        with self._lock:
            return copy(self._stop_flag.value)

    def set_status(self, value: int):
        with self._lock:
            self._status.value = value

    def get_status(self):
        with self._lock:
            return copy(self._status.value)

    def insert_input(self, obj):
        self._insert_queue(queue=self._input, obj=obj)

    def pop_input(self):
        return self._pop_queue(queue=self._input)

    def insert_output(self, obj):
        self._insert_queue(queue=self._output, obj=obj)

    def pop_output(self):
        return self._pop_queue(queue=self._output)

    def _insert_queue(self, queue: Queue, obj):
        with self._lock:
            queue.put(obj=obj, block=True, timeout=self.default_timeout_sec)

    def _pop_queue(self, queue: Queue):
        with self._lock:
            return queue.get(block=True, timeout=self.default_timeout_sec)
