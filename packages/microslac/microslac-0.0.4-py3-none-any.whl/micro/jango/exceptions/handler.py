from copy import deepcopy

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback

from micro.jango.exceptions import ApiException


def exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header  # noqa
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait  # noqa

        if isinstance(exc, ApiException):
            data = exc.detail
        else:
            codes = exc.get_codes()
            if isinstance(codes, dict):
                errors = [{"field": key, "error": next(iter(values))} for key, values in codes.items()]
            elif isinstance(codes, list):
                errors = [{"error": code} for code in codes]
            else:
                errors = [{"error": codes}]
            data = deepcopy(next(iter(errors), {}))
            if len(errors) > 1:
                data.update(errors=errors)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
