from types import SimpleNamespace

import pytest
from django.conf import settings
from faker import Factory, Faker
from rest_framework.test import APIClient

__all__ = ["factory", "client", "base_client", "internal_client"]

factory = Factory.create()


@pytest.fixture()
def client():
    api_client = APIClient()
    access_token = settings.ACCESS_TOKEN
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token}")
    api_client.token = SimpleNamespace(team="T0123456789", user="U0123456789")  # hardcoded
    return api_client


@pytest.fixture()
def base_client():
    api_client = APIClient()
    return api_client


@pytest.fixture()
def internal_client():
    api_client = APIClient()
    internal_key = settings.INTERNAL_KEY
    api_client.credentials(HTTP_X_INTERNAL=internal_key)
    return api_client


@pytest.fixture()
def fake():
    return Faker()
