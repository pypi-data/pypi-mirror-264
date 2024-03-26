import logging
import os
import resource
import socket

from frozendict import frozendict
from paho.mqtt.client import Client

from ha_services.mqtt4homeassistant.utilities.assertments import assert_uid
from ha_services.mqtt4homeassistant.utilities.system_utils import get_running_time, get_system_uptime


logger = logging.getLogger(__name__)


class BaseMqttDevice:
    device_uids = set()

    def __init__(
        self,
        *,
        name: str,
        uid: str,
        topic_prefix: str = 'homeassistant',
        manufacturer: str | None = None,
        model: str | None = None,
        sw_version: str | None = None,
    ):
        self.name = name

        assert_uid(uid)
        assert uid not in MqttDevice.device_uids, f'Duplicate uid: {uid}'
        self.uid = uid
        self.topic_prefix = topic_prefix

        self.manufacturer = manufacturer
        self.model = model
        self.sw_version = sw_version

        self._mqtt_payload_cache = None
        self.components = {}

    def register_component(self, *, component):
        from ha_services.mqtt4homeassistant.components import BaseComponent

        assert isinstance(component, BaseComponent)
        uid = component.uid
        assert uid not in self.components, f'Duplicate component: {uid}'
        self.components[uid] = component


class MqttDevice(BaseMqttDevice):
    def __init__(self, *, main_device: BaseMqttDevice | None = None, **kwargs):
        super().__init__(**kwargs)

        if main_device:
            self.via_device = main_device.uid
            self.uid = f'{main_device.uid}-{self.uid}'

    def get_mqtt_payload(self) -> dict:
        if self._mqtt_payload_cache is None:
            mqtt_payload = {
                'name': self.name,
                'identifiers': self.uid,
            }
            for key in ('via_device', 'manufacturer', 'model', 'sw_version'):
                if value := getattr(self, key, None):
                    mqtt_payload[key] = value
            self._mqtt_payload_cache = frozendict(mqtt_payload)

        return self._mqtt_payload_cache


class MainMqttDevice(MqttDevice):
    def __init__(self, **kwargs):
        assert 'main_device' not in kwargs, 'main_device is not allowed for MainMqttDevice'
        super().__init__(**kwargs)

        from ha_services.mqtt4homeassistant.components.sensor import Sensor

        self.hostname = Sensor(
            device=self,
            name='Hostname',
            uid='hostname',
        )
        self.up_time = Sensor(
            device=self,
            name='System Up Time',
            uid='up_time',
            state_class='measurement',
            unit_of_measurement='seconds',
            suggested_display_precision=0,
        )
        self.running_time = Sensor(
            device=self,
            name='Running Time',
            uid='running_time',
            state_class='measurement',
            unit_of_measurement='seconds',
            suggested_display_precision=0,
        )
        self.execute_time = Sensor(
            device=self,
            name='Execute Time',
            uid='execute_time',
            state_class='measurement',
            unit_of_measurement='seconds',
            suggested_display_precision=1,
        )
        self.system_load_1min = Sensor(
            device=self,
            name='System load 1min.',
            uid='system_load_1min',
            state_class='measurement',
            suggested_display_precision=2,
        )

    def poll_and_publish(self, client: Client) -> None:
        logger.debug(f'Polling {self.name} ({self.uid})')

        self.hostname.set_state(socket.gethostname())
        self.hostname.publish_config_and_state(client)

        self.up_time.set_state(get_system_uptime())
        self.up_time.publish_config_and_state(client)

        self.running_time.set_state(get_running_time())
        self.running_time.publish_config_and_state(client)

        self.system_load_1min.set_state(os.getloadavg()[0])
        self.system_load_1min.publish_config_and_state(client)

        usage = resource.getrusage(resource.RUSAGE_SELF)
        user_and_system_time = usage.ru_utime + usage.ru_stime
        self.execute_time.set_state(user_and_system_time)
        self.execute_time.publish_config_and_state(client)
