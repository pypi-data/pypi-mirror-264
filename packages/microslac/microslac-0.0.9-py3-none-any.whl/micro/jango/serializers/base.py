from typing import Literal

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from micro.utils import utils

ExtraHow = Literal["get", "pop"]


class BaseSerializer(Serializer):
    def pop(self, key):
        validated_data: dict = self.validated_data
        return validated_data.pop(key)

    def extract(self, *fields: str, how: ExtraHow = "pop", default=utils.unset) -> tuple:
        fields = fields or [f for f in self.fields]
        return utils.extract(self.validated_data, *fields, how=how, default=default)


class BaseModelSerializer(ModelSerializer, BaseSerializer):
    def get_fields(self):
        fields = super().get_fields()
        if exclude_fields := self.context.get("exclude_fields", []):
            fields = {key: value for key, value in fields.items() if key not in exclude_fields}
        return fields


class IdSerializer(BaseSerializer):
    id = serializers.CharField(required=True, allow_blank=False)
