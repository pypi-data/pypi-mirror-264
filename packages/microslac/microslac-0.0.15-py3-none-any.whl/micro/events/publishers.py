from __future__ import annotations

import os
import json
import pika

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from pika.exchange_type import ExchangeType


class Publisher:
    connection: BlockingConnection
    channel: BlockingChannel
    exchange: str

    def __init__(self, exchange: str):
        super().__init__()
        self.exchange = exchange
        self.setup_connection()

    def is_enabled(self) -> bool:
        return bool(int(os.getenv("RABBITMQ_ENABLED", default=0)))

    def setup_connection(self):
        if not self.is_enabled():
            return

        host = os.getenv("RABBITMQ_BROKER_HOST", default="")
        port = os.getenv("RABBITMQ_BROKER_PORT", default=0)
        username = os.getenv("RABBITMQ_BROKER_USERNAME", default="")
        password = os.getenv("RABBITMQ_BROKER_PASSWORD", default="")

        credentials = pika.PlainCredentials(username=username, password=password)
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def declare_exchange(self, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        self.channel.exchange_declare(self.exchange, exchange_type=exchange_type, **kwargs)

    def publish(
            self,
            data: dict,
            routing_key: str,
            mandatory: bool = False,
            **kwargs,
    ) -> None:
        if not self.is_enabled():
            return

        if self.connection.is_closed:
            self.setup_connection()

        data = data or {}
        body = json.dumps(data).encode("utf-8")
        properties = BasicProperties(content_encoding="utf-8", content_type="application/json", **kwargs)

        self.channel.basic_publish(
            body=body,
            exchange=self.exchange,
            routing_key=routing_key,
            properties=properties,
            mandatory=mandatory,
        )


communication = Publisher("communication")
