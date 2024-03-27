import datetime
import os

import psutil


def get_system_start_datetime() -> datetime.datetime:
    start_dt = datetime.datetime.fromtimestamp(psutil.boot_time())
    return start_dt


def process_start_datetime() -> datetime.datetime:
    p = psutil.Process(os.getpid())
    create_time: float = p.create_time()
    start_dt = datetime.datetime.fromtimestamp(create_time, datetime.timezone.utc)
    return start_dt
