"""
Middleware verifying every request to the server passes the API key validation.
"""
from django.core.exceptions import PermissionDenied
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from rest_framework_api_key.helpers import ApiKeyTestMixin


class HasAPIAccessMiddleware(MiddlewareMixin, ApiKeyTestMixin):
    """
    A custom middleware to provide API key validation for all requests that works for Django >= 1.8.
    """

    def process_request(self, request):
        """
        Middleware processing method, API key validation happens here.

        :param request: The HTTP request.
        :type request: :class:`django.http.HttpRequest`
        """

        api_key = self.get_key_from_headers(request)

        is_valid = self.is_excluded_prefix(request) or self.is_valid_key(api_key)
        if not is_valid:
            raise PermissionDenied('API key missing or invalid.')
