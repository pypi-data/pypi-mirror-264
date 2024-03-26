from django.conf import settings
from rest_framework.permissions import BasePermission


class IsInternal(BasePermission):
    def has_permission(self, request, view):
        internal_key = request.META.get("HTTP_X_INTERNAL")
        if internal_key:
            return internal_key == settings.INTERNAL_KEY
        return False
