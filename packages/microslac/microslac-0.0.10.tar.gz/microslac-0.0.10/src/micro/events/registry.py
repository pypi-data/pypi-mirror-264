from enum import StrEnum
from pika import DeliveryMode
from .base import BaseEvents, BaseProps


class Exchange(StrEnum):
    Communication = "communication"


class CommunicationEvents(BaseEvents):
    _exchange = Exchange.Communication.value
    _properties = BaseProps(delivery_mode=DeliveryMode.Persistent)
