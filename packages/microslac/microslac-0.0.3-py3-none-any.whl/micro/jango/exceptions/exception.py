from copy import deepcopy
from operator import itemgetter
from typing import List

from rest_framework import status
from rest_framework.exceptions import APIException

from micro.utils import utils


def _get_error_details(errors: List[dict]) -> dict:
    error = deepcopy(next(iter(errors)))
    if len(errors) > 1:
        error.update(errors=errors)
    return error


class ApiException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        error: str = None,
        errors: List[dict] = None,
        code: int = None,
        **kwargs,
    ):
        if error:
            error = {"error": error, **kwargs}
            errors = [error, *errors] if errors else [error]
            errors = utils.deduplicate(errors, key=itemgetter("error"))
        if not errors:
            errors = [{"error": "invalid"}]
        if code:
            self.status_code = code

        self.detail = _get_error_details(errors)
