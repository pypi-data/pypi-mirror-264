import datetime
import os
from pathlib import Path

import psutil


UPTIME_PATH = Path('/proc/uptime')


def get_system_uptime() -> float:
    content = UPTIME_PATH.read_text()
    uptime_seconds = content.split()[0]
    return float(uptime_seconds)


def get_system_start_datetime() -> datetime.datetime:
    uptime_sec = get_system_uptime()
    start_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=uptime_sec)
    return start_dt


def process_start_datetime() -> datetime.datetime:
    p = psutil.Process(os.getpid())
    create_time: float = p.create_time()
    start_dt = datetime.datetime.fromtimestamp(create_time, datetime.timezone.utc)
    return start_dt
