import datetime
from unittest import TestCase

from ha_services.mqtt4homeassistant.utilities.system_utils import (
    get_system_start_datetime,
    get_system_uptime,
    process_start_datetime,
)


class SystemUtilsTestCase(TestCase):
    def test_get_system_uptime(self):
        uptime = get_system_uptime()
        self.assertIsInstance(uptime, float)
        self.assertGreater(uptime, 0)

    def test_get_system_start_datetime(self):
        start_dt = get_system_start_datetime()
        self.assertIsInstance(start_dt, datetime.datetime)

    def test_process_start_datetime(self):
        start_dt = process_start_datetime()
        self.assertIsInstance(start_dt, datetime.datetime)
