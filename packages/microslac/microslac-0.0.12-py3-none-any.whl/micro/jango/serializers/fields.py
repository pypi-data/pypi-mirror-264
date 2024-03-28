from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    default_error_messages = {
        "invalid": _("Timestamp has wrong format. Use one of these formats instead: {format}."),
    }

    def to_representation(self, value: datetime):
        if not value:
            return None
        if self.context.get("round_ts", False):
            return round(value.timestamp() * 1e3)
        return value.timestamp()

    def to_internal_value(self, value):
        if not value:
            return None

        if isinstance(value, datetime):
            return timezone.make_naive(value, timezone.utc)

        try:
            value = float(value)
        except (TypeError, ValueError):
            self.fail("invalid")

        dt_value = None
        for val in (value, value / 1e3):
            try:
                dt_value = datetime.utcfromtimestamp(val)
            except (TypeError, ValueError):
                pass
            else:
                break

        if dt_value is None:
            self.fail("invalid")

        if timezone.is_aware(dt_value):
            return timezone.make_naive(dt_value, timezone.utc)
        return dt_value
