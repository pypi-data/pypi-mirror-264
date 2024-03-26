import time
from functools import cache
from pathlib import Path


UPTIME_PATH = Path('/proc/uptime')


def get_system_uptime() -> float:
    content = UPTIME_PATH.read_text()
    uptime_seconds = content.split()[0]
    return float(uptime_seconds)


@cache
def global_start_time() -> int:
    return int(time.monotonic())


def get_running_time() -> int:
    return int(time.monotonic() - global_start_time())
