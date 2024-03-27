from string import ascii_uppercase, digits
from typing import Any

from shortuuid.django_fields import ShortUUIDField


class ShortIdField(ShortUUIDField):
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs["length"] = kwargs.get("length", 11)
        kwargs["max_length"] = kwargs.get("max_length", 20)
        kwargs["alphabet"] = kwargs.get("alphabet", ascii_uppercase + digits)
        super().__init__(*args, **kwargs)
