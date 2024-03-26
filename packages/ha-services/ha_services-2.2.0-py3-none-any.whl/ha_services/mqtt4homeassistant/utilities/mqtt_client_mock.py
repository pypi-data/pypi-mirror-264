from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager


class MqttClientMock:
    def __init__(self):
        self.messages = []

    def publish(self, **kwargs) -> None:
        self.messages.append(kwargs)


class MainMqttDeviceMock(MassContextManager):
    def __init__(self):
        class UsageMock:
            ru_utime = 1
            ru_stime = 1

        self.mocks = (
            patch('ha_services.mqtt4homeassistant.device.socket.gethostname', return_value='TheHostName'),
            patch('ha_services.mqtt4homeassistant.device.get_system_uptime', return_value=123),
            patch('ha_services.mqtt4homeassistant.device.get_running_time', return_value=12),
            patch('ha_services.mqtt4homeassistant.device.os.getloadavg', return_value=(1, 2, 3)),
            patch('ha_services.mqtt4homeassistant.device.resource.getrusage', return_value=UsageMock),
        )
