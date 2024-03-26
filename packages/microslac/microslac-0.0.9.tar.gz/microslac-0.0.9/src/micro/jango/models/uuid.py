import uuid

from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True
