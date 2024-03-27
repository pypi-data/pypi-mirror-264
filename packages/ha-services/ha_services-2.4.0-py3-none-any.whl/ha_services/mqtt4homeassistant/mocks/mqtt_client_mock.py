from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager

from ha_services.mqtt4homeassistant.mocks.psutil_mock import PsutilMock


class MqttClientMock:
    def __init__(self):
        self.messages = []

    def publish(self, **kwargs) -> None:
        self.messages.append(kwargs)


class MainMqttDeviceMock(MassContextManager):
    def __init__(self):

        psutil_mock = PsutilMock()

        self.mocks = (
            patch('ha_services.mqtt4homeassistant.device.socket.gethostname', return_value='TheHostName'),
            #
            patch('ha_services.mqtt4homeassistant.system_info.cpu.psutil', psutil_mock),
            patch('ha_services.mqtt4homeassistant.system_info.memory.psutil', psutil_mock),
            patch('ha_services.mqtt4homeassistant.system_info.temperatures.psutil', psutil_mock),
        )
