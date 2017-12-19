from django.conf import settings
from rest_framework import permissions
from rest_framework_api_key.models import APIKey

# Loaded dynamically to handle cases where the settings variable is not defined.
excluded_prefixes = getattr(settings, 'API_KEY_MIDDLEWARE_EXCLUDED_URL_PREFIXES', ())


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view=None):
        api_key = request.META.get('HTTP_API_KEY', '')
        return request.path.startswith(excluded_prefixes) or APIKey.objects.filter(key=api_key).exists()
