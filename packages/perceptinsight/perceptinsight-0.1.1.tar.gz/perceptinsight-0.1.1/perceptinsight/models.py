from dataclasses import dataclass
from typing import Optional, Dict, List, Any, Union
from enum import Enum


class DEFAULT_USER_PROPERTIES_KEYS(Enum):
    USER_ID = 'user_id'
    PHONE = 'phone'
    EMAIL = 'email'
    DEVICE_TOKEN = 'device_token'
    NAME = 'name'


@dataclass
class DeviceProperties:
    pi_sdk_type: Optional[str]


@dataclass
class InitOptions:
    autoFlushThresholdMs: Optional[int] = None
    autoFlushBatchSize: Optional[int] = None
    maxApiRetry: Optional[int] = None


@dataclass
class EventData:
    data: Optional[Dict[str, any]]
    multiData: Optional[Dict[str, List[any]]]


@dataclass
class TrackingEventRequest(EventData):
    name: str

    def to_dict(self):
        return {
            'name': self.name,
            'data': self.data,
            'multiData': self.multiData
        }


@dataclass
class TrackingUserRequest(EventData):
    userId: str

    def to_dict(self):
        return {
            'userId': self.userId,
            'data': self.data,
            'multiData': self.multiData
        }


UserProperties = Dict[Union[str, DEFAULT_USER_PROPERTIES_KEYS], Union[str, int, List[Union[str, int]]]]
