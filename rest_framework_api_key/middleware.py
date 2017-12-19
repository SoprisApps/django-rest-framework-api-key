"""
Middleware verifying every request to the server passes the API key validation.
"""
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from rest_framework_api_key.helpers import get_key_from_headers
from rest_framework_api_key.models import APIKey


# Loaded dynamically to handle cases where the settings variable is not defined.
excluded_prefixes = getattr(settings, 'API_KEY_MIDDLEWARE_EXCLUDED_URL_PREFIXES', ())


class APIKeyMiddleware(MiddlewareMixin):
    """
    A custom middleware to provide API key validation for all requests that works for Django >= 1.8.
    """

    def is_key_valid(self, api_key):
        """
        A wrapper function around api key validation, to make the
        process more generic and easier to mock.

        :param api_key: The api key value from the request.
        :type api_key: str
        :return: Whether the key has been registered.
        :rtype: bool
        """
        return APIKey.is_valid(api_key)

    def process_request(self, request):
        """
        Middleware processing method, API key validation happens here.

        :param request: The HTTP request.
        :type request: :class:`django.http.HttpRequest`
        """
        api_key = get_key_from_headers(request)
        api_key_object = APIKey.objects.filter(key=api_key).first()

        is_valid = (
            self.is_key_valid(api_key) or
            request.path.startswith(excluded_prefixes))
        if not is_valid:
            raise PermissionDenied('API key missing or invalid.')

        request.api_key = api_key_object
