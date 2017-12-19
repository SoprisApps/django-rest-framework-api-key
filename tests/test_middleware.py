import django
from django.core.urlresolvers import reverse

from tests.test_admin import APIAuthenticatedTestCase


class APIMiddlewareTest(APIAuthenticatedTestCase):
    """
    Test authentication using API key middleware.
    """

    def setUp(self):
        self.override_settings(REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES':
                ('rest_framework.permissions.AllowAny',),
        })

        middleware = {
            'append': 'rest_framework_api_key.middleware.APIKeyMiddleware'
        }
        if django.VERSION >= (1, 10):
            # in Django 1.10, MIDDLEWARE_CLASSES was changed to MIDDLEWARE
            self.modify_settings(MIDDLEWARE=middleware)
        else:
            self.modify_settings(MIDDLEWARE_CLASSES=middleware)

    def test_get_view_authorized(self):
        """
        Test successful authentication.
        """
        response = self.client.get(reverse("test-view"), **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["msg"], "Hello World!")

    def test_get_view_unauthorized(self):
        """
        Test failed authentication.
        """
        response = self.client.get(reverse("test-view"))

        self.assertEqual(response.status_code, 403)

    def test_get_view_excluded(self):
        """
        Test not required for paths excluded in settings.
        """
        response = self.client.get(reverse("admin:index"))
        self.assertNotEqual(response.status_code, 403)
