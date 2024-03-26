import json
from types import SimpleNamespace

import pytest
from faker import Factory
from rest_framework.test import APIClient

__all__ = ["ApiTestBase", "UnitTestBase"]


@pytest.mark.django_db(databases=["default", "replication"])
class ApiTestBase:
    fake = Factory.create()
    client: APIClient
    base_client: APIClient
    internal_client: APIClient

    @pytest.fixture(autouse=True)
    def setup(self, client, base_client, internal_client):
        self.client = client
        self.base_client = base_client
        self.internal_client = internal_client

    def client_request(
        self,
        url: str,
        *,
        method: str = None,
        data: dict = None,
        format: str = None,
        ok: bool = None,
        status: int = None,
        base: bool = False,
        internal: bool = False,
        client: APIClient = None
    ):
        data = data or {}
        format = format or "json"
        method = method or "post"
        assert method in ("get", "post", "put", "patch", "delete")

        if base:
            client = self.base_client
        elif internal:
            client = self.internal_client
        elif client is None:
            client = self.client

        client_method = getattr(client, method)
        response = client_method(url, data=data, format=format)

        if status is not None:
            if response.status_code != status:
                try:
                    error = response.json()
                except ValueError:
                    error = response.content.decode("utf-8")
                raise Exception(error)  # debug

        resp = self.objectify(response.data)

        if ok is not None:
            assert resp.ok == ok

        return resp

    @staticmethod
    def objectify(data: dict):
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))


@pytest.mark.django_db(databases=["default", "replication"])
class UnitTestBase:
    def objectify(self, data: dict):
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
