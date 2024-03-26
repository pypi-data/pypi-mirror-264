import os
import re
from types import SimpleNamespace
from urllib import parse

import requests

from micro.utils import utils


class ServiceMeta(type):
    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        svc = getattr(cls, "name", name.removesuffix("Service"))
        NAME = re.sub(r"(?<!^)(?=[A-Z])", "_", svc).upper()  # noqa
        MICROSERVICE = f"MICROSERVICE_{NAME}"  # noqa
        MICROSERVICE_ALL = "MICROSERVICE_ALL"  # noqa

        if override_scheme := os.getenv(MICROSERVICE + "_SCHEME", default=""):
            cls.scheme = override_scheme
        if override_queue := os.getenv(MICROSERVICE + "_QUEUE", default=""):
            cls.queue = override_queue
        if override_host := os.getenv(MICROSERVICE + "_HOST", default=""):
            cls.host = override_host
        if override_all_host := os.getenv(MICROSERVICE_ALL + "_HOST", default=""):
            cls.host = override_all_host
        if override_port := os.getenv(MICROSERVICE + "_PORT", default=0):
            cls.port = int(override_port)
        if override_key := os.getenv(MICROSERVICE + "_KEY", default=0):
            cls.key = int(override_key)
        return cls


class Service(metaclass=ServiceMeta):
    scheme: str = "http"
    queue: str = ""
    host: str
    port: int
    key: str

    @classmethod
    def get_url(cls, path: str) -> str:
        scheme = cls.scheme
        netloc = f"{cls.host}:{cls.port}"
        url = parse.urlunsplit((scheme, netloc, path, "", ""))
        return url

    @classmethod
    def get_base_headers(cls, internal: bool = False) -> dict[str, str]:
        base_headers = {}
        if internal:
            internal_key = os.getenv("MICROSERVICE_INTERNAL_KEY", default="internal")
            base_headers.update({"X-Internal": internal_key})
        return base_headers

    @classmethod
    def post(
        cls,
        path,
        data: dict,
        internal: bool = True,
        key: str = None,
        keys: list[str] = None,
        objectify: bool = False,
        raise_for_status: bool = True,
        **kwargs,
    ) -> dict | SimpleNamespace:
        data = data or {}
        url = cls.get_url(path)
        headers = kwargs.pop("headers", {})
        base_headers = cls.get_base_headers(internal=internal)
        response = requests.post(url=url, json=data, headers={**headers, **base_headers}, **kwargs)
        if raise_for_status:
            response.raise_for_status()
        resp = response.json()
        if key:
            resp = resp.get(key)
        if keys:
            resp = {key: resp.get(key) for key in keys}
        if objectify:
            resp = utils.objectify(resp)
        return resp
