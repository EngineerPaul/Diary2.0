from django.conf import settings
from rest_framework import permissions

from utils.service_auth import SERVICE_TOKEN_HEADER


class ServiceTokenPermission(permissions.BasePermission):
    """Internal service-to-service requests only."""

    def has_permission(self, request, view):
        expected = settings.INTERNAL_SERVICE_TOKEN
        if not expected:
            return False
        return request.headers.get(SERVICE_TOKEN_HEADER) == expected
