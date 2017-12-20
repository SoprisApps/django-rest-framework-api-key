import binascii
from django.conf import settings
import os
import re

from rest_framework_api_key.models import APIKey

default_header_token = 'api-key'
header_token_setting = getattr(settings, 'REST_FRAMEWORK_API_KEY_HEADER_TOKEN', default_header_token)
header_token = "HTTP_%s" % (re.sub('-', '_', header_token_setting.upper()))

# Loaded dynamically to handle cases where the settings variable is not defined.
excluded_prefixes = getattr(settings, 'REST_FRAMEWORK_API_KEY_MIDDLEWARE_EXCLUDED_URL_PREFIXES', ())


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class ApiKeyTestMixin:
    def get_key_from_headers(self, request):
        return request.META.get(header_token, '')

    def is_excluded_prefix(self, request):
        return request.path.startswith(excluded_prefixes)

    def is_valid_key(self, api_key):
        return APIKey.objects.filter(key=api_key).exists()
