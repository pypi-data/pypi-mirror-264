from __future__ import annotations

import json

from django.conf import settings
from pika import BasicProperties, BlockingConnection, ConnectionParameters, PlainCredentials
from pika.channel import Channel
from pika.connection import Connection
from pika.exchange_type import ExchangeType


class ConnectionDescriptor:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls: type[BaseQueue]):
        if instance is not None:
            raise RuntimeError("Cannot access class attributes from concrete instance.")

        if not all([self.host, self.port, self.username, self.password]):
            raise RuntimeError("Required all connection options.")

        # TODO: global connection pool, fast + jango
        credentials = PlainCredentials(username=self.username, password=self.password)
        parameters = ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        connection = BlockingConnection(parameters=parameters)
        setattr(cls, self.name, connection)
        return connection


class ChannelDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls: type[BaseQueue]):
        if instance is not None:
            raise RuntimeError("Cannot access class attributes from concrete instance.")

        channel = cls._connection.channel()
        setattr(cls, self.name, channel)
        return channel


class BaseQueue:
    _connection: Connection = ConnectionDescriptor(
        host=getattr(settings, "RABBITMQ_BROKER_HOST", None),
        port=getattr(settings, "RABBITMQ_BROKER_PORT", None),
        username=getattr(settings, "RABBITMQ_BROKER_USERNAME", None),
        password=getattr(settings, "RABBITMQ_BROKER_PASSWORD", None),
    )
    _channel: Channel = ChannelDescriptor()
    _exchange: str

    @classmethod
    def publish(
        cls,
        data: dict,
        routing_key: str,
        exchange: str = "",
        mandatory: bool = False,
        properties: BasicProperties = None,
        **kwargs,
    ):
        data = data or {}
        exchange = exchange or cls._exchange
        body = json.dumps(data).encode("utf-8")
        properties = properties or BasicProperties(content_type="application/json", content_encoding="utf-8", **kwargs)

        cls._channel.basic_publish(
            body=body,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
        )

    @classmethod
    def get_exchange(cls) -> str:
        return cls._exchange

    @classmethod
    def get_channel(cls) -> Channel:
        return cls._channel

    @classmethod
    def declare_exchange(cls, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        exchange = cls.get_exchange()
        channel = cls.get_channel()
        channel.exchange_declare(exchange, exchange_type=exchange_type, **kwargs)
