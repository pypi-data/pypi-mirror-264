import logging
import os
import platform
import signal
from datetime import datetime
from logging import Logger
from typing import Optional
from uuid import uuid4


def force_kill_process(pid: int):
    system = platform.system()
    print(f"Force killing {pid=}")
    if system == "Windows":
        os.system(f"taskkill /f /pid {pid}")
    else:
        os.kill(pid, signal.SIGKILL)


def generate_id(time: Optional[datetime] = None, uuid_length: int = 6):
    time = time or datetime.now()
    time_part = time.strftime("%H%M_%d%m_")
    uuid_part = str(uuid4()).replace("-", "")[:uuid_length]
    return time_part + uuid_part


def setup_logger():
    logger = Logger(name=__name__, level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(process)d:%(message)s')
    handler.setLevel(level=logging.INFO)
    handler.setFormatter(fmt=formatter)
    logger.addHandler(hdlr=handler)
    return logger
