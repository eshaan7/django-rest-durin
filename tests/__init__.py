from django.contrib.auth import get_user_model
from django.core.cache import cache as default_cache
from rest_framework.test import APITestCase

from durin.models import AuthToken, Client

User = get_user_model()


class CustomTestCase(APITestCase):
    def setUp(self):
        # cleanup
        default_cache.clear()
        AuthToken.objects.all().delete()
        Client.objects.all().delete()
        # setup
        self.authclient = Client.objects.create(name="authclientfortest")
        username = "john.doe"
        email = "john.doe@example.com"
        password = "hunter2"
        self.user = User.objects.create_user(username, email, password)
        self.creds = {
            "username": username,
            "password": password,
            "client": self.authclient.name,
        }

        username2 = "jane.doe"
        email2 = "jane.doe@example.com"
        password2 = "hunter2"
        self.user2 = User.objects.create_user(username2, email2, password2)
        self.creds2 = {
            "username": username2,
            "password": password2,
            "client": self.authclient.name,
        }

        self.client_names = ["web", "mobile", "cli"]
