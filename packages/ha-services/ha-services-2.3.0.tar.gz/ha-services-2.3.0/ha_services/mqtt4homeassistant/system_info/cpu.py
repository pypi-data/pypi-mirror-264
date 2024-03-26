import psutil

from ha_services.mqtt4homeassistant.components.sensor import Sensor


class CpuFreqSensor(Sensor):
    """
    Sensor for the system up time.
    Adds the datetime when the system was started to Home Assistant.
    """

    def __init__(self, **kwargs):
        # https://www.home-assistant.io/integrations/sensor/#device-class
        kwargs.setdefault('device_class', 'frequency')
        kwargs.setdefault('name', 'CPU frequency')
        kwargs.setdefault('uid', 'cpu_freq')
        kwargs.setdefault('unit_of_measurement', 'Mhz')
        super().__init__(**kwargs)

        info = psutil.cpu_freq()
        self.set_state(info.current)
