from django.core.urlresolvers import reverse
from django.test import override_settings
from tests.test_admin import APIAuthenticatedTestCase, APIAuthenticatedTestCaseAlternateHeaderToken


class APICategoriesEndpoint(APIAuthenticatedTestCase):

    def test_get_view_authorized(self):

        response = self.client.get(reverse("test-view"), **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["msg"], "Hello World!")

    def test_get_view_unauthorized(self):

        response = self.client.get(reverse("test-view"))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")


@override_settings(REST_FRAMEWORK_API_KEY_HEADER_TOKEN='custom-api-key')
class APICategoriesEndpointAlternateHeaderToken(APIAuthenticatedTestCaseAlternateHeaderToken):

    def test_get_view_authorized(self):

        response = self.client.get(reverse("test-view"), **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["msg"], "Hello World!")

    def test_get_view_unauthorized(self):

        response = self.client.get(reverse("test-view"))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
