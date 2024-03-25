from __future__ import annotations

import dataclasses
from typing import TypeAlias

from bx_py_utils.anonymize import anonymize


StatePayload: TypeAlias = str | bytes | bytearray | int | float | None


@dataclasses.dataclass
class ComponentState:
    topic: str
    payload: StatePayload


@dataclasses.dataclass
class ComponentConfig:
    topic: str
    payload: dict


@dataclasses.dataclass
class MqttSettings:
    """
    Credentials to MQTT server that should be used.
    """

    host: str = 'mqtt.eclipseprojects.io'  # public test MQTT broker service
    port: int = 1883
    user_name: str = ''
    password: str = ''

    def anonymized(self):
        data = dataclasses.asdict(self)
        if self.password:
            data['password'] = anonymize(self.password)
        return data
