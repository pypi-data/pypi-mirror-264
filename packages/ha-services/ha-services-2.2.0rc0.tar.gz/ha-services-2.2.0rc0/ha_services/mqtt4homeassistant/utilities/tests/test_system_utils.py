from unittest import TestCase

from ha_services.mqtt4homeassistant.utilities.system_utils import get_running_time, get_system_uptime


class SystemUtilsTestCase(TestCase):
    def test_get_system_uptime(self):
        uptime = get_system_uptime()
        self.assertIsInstance(uptime, float)
        self.assertGreater(uptime, 0)

    def test_get_running_time(self):
        running_time = get_running_time()
        self.assertIsInstance(running_time, int)
        self.assertGreaterEqual(running_time, 0)
