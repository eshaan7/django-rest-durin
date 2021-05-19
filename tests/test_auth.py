from importlib import reload

from django.db import reset_queries
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from durin import auth
from durin.models import AuthToken, Client
from durin.settings import durin_settings

from . import CustomTestCase

root_url = reverse("api-root")

new_settings = durin_settings.defaults.copy()


class AuthTestCase(CustomTestCase):
    def setUp(self):
        super().setUp()
        # authenticate client
        self.token_instance = AuthToken.objects.create(self.user, self.authclient)
        self.client.credentials(
            HTTP_AUTHORIZATION=("Token %s" % self.token_instance.token)
        )
        # reset queries
        reset_queries()
        self.assertNumQueries(0, msg="Queries were reset")

    def test_authtoken_lookup_1_sql_query(self):
        with self.assertNumQueries(
            1,
            msg="Since we use ``select_related`` it should take only 1 query",
        ):
            resp = self.client.get(root_url)
            self.assertEqual(resp.status_code, 200)

    def test_authtoken_lookup_2_sql_query(self):
        # override settings
        new_settings["AUTHTOKEN_SELECT_RELATED_LIST"] = False
        with override_settings(REST_DURIN=new_settings):
            reload(auth)
            with self.assertNumQueries(
                2,
                msg="Since we didn't use ``select_related`` it should take 2 queries",
            ):
                resp = self.client.get(root_url)
                self.assertEqual(resp.status_code, 200)

    def test_update_token_key(self):
        self.assertEqual(AuthToken.objects.count(), 1)
        self.assertEqual(Client.objects.count(), 1)
        rf = APIRequestFactory()
        request = rf.get("/")
        request.META = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.token_instance.token)
        }
        (auth_user, auth_token) = auth.TokenAuthentication().authenticate(request)
        self.assertEqual(
            self.token_instance.token,
            auth_token.token,
        )
        self.assertEqual(self.user, auth_user)
