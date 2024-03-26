from django.db import models
from django.utils import timezone

from micro.jango.models.manager import BaseManager, BaseQuerySet


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeletedQuerySet(BaseQuerySet):
    def delete(self, deleter_id: str = ""):
        for obj in self:
            obj.delete(deleter_id, save=False)
        return self.bulk_update(self, ["deleted", "deleter_id"])

    def destroy(self):
        for obj in self:
            obj.destroy()


class DeletedManager(BaseManager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, using=self._db).filter(deleted__isnull=True)

    def include_deleted(self):
        return DeletedQuerySet(self.model, using=self._db)


class DeletedModel(models.Model):
    deleted = models.DateTimeField(null=True)
    deleter_id = models.CharField(max_length=20, default="")

    class Meta:
        abstract = True

    objects = DeletedManager()

    def delete(self, deleter_id: str = "", save: bool = True):
        if not self.deleted:
            self.deleted = timezone.now()
            self.deleter_id = deleter_id or self.deleter_id
            if save:
                self.save()

    def restore(self, save: bool = True):
        if self.deleted:
            self.deleted = None
            self.deleter_id = ""
            if save:
                self.save()

    def destroy(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)


class HistoryModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator_id = models.CharField(max_length=20, default="")
    updater_id = models.CharField(max_length=20, default="")

    class Meta:
        abstract = True
