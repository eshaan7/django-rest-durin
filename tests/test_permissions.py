from django.urls import reverse
from rest_framework import status

from durin.models import AuthToken, Client
from example_project.permissions import TEST_CLIENT_NAME

from . import CustomTestCase

restricted_allow_url = reverse("restricted_allow-api")
restricted_disallow_url = reverse("restricted_disallow-api")


class PermissionsTestCase(CustomTestCase):
    def setUp(self):
        super().setUp()
        # authenticate client
        Client.objects.all().delete()
        self.token1 = AuthToken.objects.create(
            self.user, Client.objects.create(name=TEST_CLIENT_NAME)
        )

        self.token2 = AuthToken.objects.create(
            self.user, Client.objects.create(name="someotherclient")
        )

    def test_restricted_allow_view_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % self.token1.token))
        resp = self.client.get(restricted_allow_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_restricted_allow_view_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % self.token2.token))
        resp = self.client.get(restricted_allow_url)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_restricted_disallow_view_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % self.token1.token))
        resp = self.client.get(restricted_disallow_url)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_restricted_disallow_view_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % self.token2.token))
        resp = self.client.get(restricted_disallow_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
