import abc
import json
import logging

from frozendict import frozendict
from paho.mqtt.client import Client, MQTTMessageInfo

from ha_services.mqtt4homeassistant.data_classes import ComponentConfig, ComponentState
from ha_services.mqtt4homeassistant.device import MqttDevice, get_origin_data
from ha_services.mqtt4homeassistant.utilities.assertments import assert_uid


logger = logging.getLogger(__name__)


class BaseComponent(abc.ABC):
    def __init__(
        self,
        *,
        device: MqttDevice,
        name: str,
        uid: str,
        component: str,
    ):
        self.device = device

        self.name = name

        assert_uid(uid)
        self.uid = f'{self.device.uid}-{uid}'

        assert component
        self.component = component
        self.device.register_component(component=self)

        # e.g.: 'homeassistant/sensor/My-device/Chip-Temperature'
        self.topic_prefix = f'{self.device.topic_prefix}/{self.component}/{self.device.uid}/{self.uid}'

        self._config_kwargs_cache = None

    def _get_config_kwargs(self) -> dict:
        if self._config_kwargs_cache is None:
            config: ComponentConfig = self.get_config()
            payload = config.payload
            payload['origin'] = get_origin_data()
            payload = json.dumps(config.payload, ensure_ascii=False, sort_keys=True)
            self._config_kwargs_cache = frozendict(
                {
                    'topic': config.topic,
                    'payload': payload,
                }
            )
        return self._config_kwargs_cache

    def publish_config(self, client: Client) -> MQTTMessageInfo:
        config_kwargs = self._get_config_kwargs()
        logger.debug(f'Publishing {self.uid=} config: {config_kwargs}')
        info: MQTTMessageInfo = client.publish(**config_kwargs)
        return info

    def publish_state(self, client: Client) -> MQTTMessageInfo:
        state: ComponentState = self.get_state()
        info: MQTTMessageInfo = client.publish(topic=state.topic, payload=state.payload)
        return info

    def publish_config_and_state(self, client: Client) -> tuple[MQTTMessageInfo, MQTTMessageInfo]:
        config_info = self.publish_config(client)
        state_info = self.publish_state(client)
        return config_info, state_info

    @abc.abstractmethod
    def get_state(self) -> ComponentState:
        pass

    @abc.abstractmethod
    def get_config(self) -> ComponentConfig:
        pass
