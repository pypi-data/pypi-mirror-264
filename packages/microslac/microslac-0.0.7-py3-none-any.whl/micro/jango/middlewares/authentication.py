import jwt
from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class TokenData:
    __slots__ = ("auth", "team", "user")

    def __init__(self, data: dict):
        self.auth = data.pop("aid")
        self.team = data.get("tid")
        self.user = data.get("uid")


def get_token_data(request: Request):
    try:
        auth = get_authorization_header(request).split()
        access = auth[1].decode()
        access_data = jwt.decode(jwt=access, options={"verify_signature": False})
        token = TokenData(access_data)
        return token
    except Exception as ex:
        raise AuthenticationFailed() from ex


class JwtTokenMiddleware:
    def __init__(self, get_response: callable):
        self.get_response = get_response

    def __call__(self, request: Request):
        request.token = SimpleLazyObject(lambda: get_token_data(request))
        response = self.get_response(request)
        return response
