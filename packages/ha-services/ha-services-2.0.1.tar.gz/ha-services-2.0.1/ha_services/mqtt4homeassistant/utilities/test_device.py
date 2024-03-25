from unittest import TestCase

from ha_services.mqtt4homeassistant.device import MqttDevice


class DeviceTestCase(TestCase):
    def test_device(self):
        device = MqttDevice(name='My device', uid='device_id')
        self.assertEqual(device.get_mqtt_payload(), {'name': 'My device', 'identifiers': 'device_id'})
