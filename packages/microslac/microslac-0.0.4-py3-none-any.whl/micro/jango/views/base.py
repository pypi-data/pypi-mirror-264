from functools import partial

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from micro.jango.constants import Const


class BaseViewSet(ViewSet):
    pass


class HttpMethod(Const):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    HEAD = "head"
    OPTIONS = "options"
    TRACE = "trace"


post = partial(action, methods=[HttpMethod.POST], detail=False)


def unauthorized(request):
    return HttpResponse("Unauthorized", status=status.HTTP_403_FORBIDDEN)
