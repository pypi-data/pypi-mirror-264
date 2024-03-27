from __future__ import annotations

import os
import json

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

    def __get__(self, instance, cls: type[BaseEvents]):
        if instance is not None:
            raise RuntimeError("Cannot access class attributes from concrete instance.")

        if not all([self.host, self.port, self.username, self.password]):
            raise RuntimeError("Required all connection options.")

        credentials = PlainCredentials(username=self.username, password=self.password)
        parameters = ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        connection = BlockingConnection(parameters=parameters)
        setattr(cls, self.name, connection)
        return connection


class ChannelDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls: type[BaseEvents]):
        if instance is not None:
            raise RuntimeError("Cannot access class attributes from concrete instance.")

        channel = cls._connection.channel()
        setattr(cls, self.name, channel)
        return channel


class BaseProps(BasicProperties):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("content_encoding", "utf-8")
        kwargs.setdefault("content_type", "application/json")
        super().__init__(*args, **kwargs)


class BaseEvents:
    _connection: Connection = ConnectionDescriptor(
        host=os.getenv("RABBITMQ_BROKER_HOST", default=""),
        port=os.getenv("RABBITMQ_BROKER_PORT", default=0),
        username=os.getenv("RABBITMQ_BROKER_USERNAME", default=None),
        password=os.getenv("RABBITMQ_BROKER_PASSWORD", default=None),
    )
    _channel: Channel = ChannelDescriptor()
    _properties: BasicProperties
    _exchange: str

    @classmethod
    def get_exchange(cls) -> str:
        return cls._exchange

    @classmethod
    def get_channel(cls) -> Channel:
        return cls._channel

    @classmethod
    def declare_exchange(cls, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        channel = cls.get_channel()
        exchange = cls.get_exchange()
        channel.exchange_declare(exchange, exchange_type=exchange_type, **kwargs)

    @classmethod
    def publish(
            cls,
            data: dict,
            routing_key: str,
            mandatory: bool = False,
            **kwargs,
    ):
        data = data or {}
        exchange = cls._exchange
        body = json.dumps(data).encode("utf-8")
        properties = cls._properties or BaseProps(**kwargs)

        cls._channel.basic_publish(
            body=body,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
        )
