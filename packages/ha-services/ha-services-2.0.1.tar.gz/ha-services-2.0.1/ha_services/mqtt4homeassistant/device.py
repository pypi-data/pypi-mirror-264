from functools import cache

from frozendict import frozendict

import ha_services
from ha_services.mqtt4homeassistant.utilities.assertments import assert_uid


@cache
def get_origin_data() -> dict:
    return {
        'name': 'ha-services',
        'sw_version': ha_services.__version__,
        'support_url': 'https://pypi.org/project/ha_services/',
    }


class MqttDevice:
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

    def get_mqtt_payload(self) -> dict:
        if self._mqtt_payload_cache is None:
            mqtt_payload = {'name': self.name, 'identifiers': self.uid}
            for key in ('manufacturer', 'model', 'sw_version'):
                if getattr(self, key):
                    mqtt_payload[key] = getattr(self, key)
            self._mqtt_payload_cache = frozendict(mqtt_payload)

        return self._mqtt_payload_cache
