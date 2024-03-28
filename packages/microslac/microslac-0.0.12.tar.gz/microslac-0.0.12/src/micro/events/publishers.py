from __future__ import annotations

import os
import json
import pika
import threading

from pika.channel import Channel
from pika.connection import Connection
from pika.exchange_type import ExchangeType


class ConnectionDescriptor:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __get__(self, instance: Publisher, cls: type[Publisher]):
        if instance is None:
            return self

        if not all([self.host, self.port, self.username, self.password]):
            raise RuntimeError("Required all connection parameters.")

        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        res = instance._connection = pika.BlockingConnection(parameters=parameters)
        return res


class ChannelDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance: Publisher, cls: type[Publisher]):
        if instance is None:
            return self

        res = instance._channel = instance._connection.channel()  # noqa
        return res


class BaseProperties(pika.BasicProperties):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("content_encoding", "utf-8")
        kwargs.setdefault("content_type", "application/json")
        super().__init__(*args, **kwargs)


class Publisher(threading.Thread):
    _connection: Connection = ConnectionDescriptor(
        host=os.getenv("RABBITMQ_BROKER_HOST", default=""),
        port=os.getenv("RABBITMQ_BROKER_PORT", default=0),
        username=os.getenv("RABBITMQ_BROKER_USERNAME", default=None),
        password=os.getenv("RABBITMQ_BROKER_PASSWORD", default=None),
    )
    _channel: Channel = ChannelDescriptor()
    _properties: pika.BasicProperties
    _exchange: str

    def __init__(self, exchange: str, properties: pika.BasicProperties = None):
        super().__init__()
        self._properties = properties or BaseProperties()
        self._exchange = exchange

    def get_exchange(self) -> str:
        return self._exchange

    def get_channel(self) -> Channel:
        return self._channel

    def declare_exchange(self, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        channel = self.get_channel()
        exchange = self.get_exchange()
        channel.exchange_declare(exchange, exchange_type=exchange_type, **kwargs)

    def publish(
            self,
            data: dict,
            routing_key: str,
            mandatory: bool = False,
            **kwargs,
    ):
        data = data or {}
        exchange = self._exchange
        properties = self._properties
        body = json.dumps(data).encode("utf-8")

        self._channel.basic_publish(
            body=body,
            exchange=exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
        )


communication = Publisher("communication")
