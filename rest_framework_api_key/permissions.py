from django.conf import settings
from rest_framework import permissions
from rest_framework_api_key.helpers import ApiKeyTestMixin

# Loaded dynamically to handle cases where the settings variable is not defined.
excluded_prefixes = getattr(settings, 'API_KEY_MIDDLEWARE_EXCLUDED_URL_PREFIXES', ())


class HasAPIAccess(permissions.BasePermission, ApiKeyTestMixin):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view=None):
        api_key = self.get_key_from_headers(request)
        return self.is_valid_key(api_key)
