"""
Middleware verifying every request to the server passes the API key validation.
"""
from django.core.exceptions import PermissionDenied
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from rest_framework.request import Request
from rest_framework_api_key.permissions import HasAPIAccess


class APIKeyMiddleware(MiddlewareMixin):
    """
    A custom middleware to provide API key validation for all requests that works for Django >= 1.8.
    """

    def process_request(self, request):
        """
        Middleware processing method, API key validation happens here.

        :param request: The HTTP request.
        :type request: :class:`django.http.HttpRequest`
        """
        permission_object = HasAPIAccess()

        if not permission_object.has_permission(Request(request)):
            raise PermissionDenied('API key missing or invalid.')
