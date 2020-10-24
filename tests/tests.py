import time
from datetime import timedelta
from importlib import reload

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework.serializers import DateTimeField
from rest_framework.test import APIRequestFactory, APITestCase

from durin import views
from durin.auth import TokenAuthentication
from durin.models import AuthToken, Client
from durin.serializers import UserSerializer
from durin.settings import durin_settings
from durin.signals import token_expired, token_renewed

User = get_user_model()
root_url = reverse("api-root")
cached_auth_url = reverse("cached-auth-api")
login_url = reverse("durin_login")
logout_url = reverse("durin_logout")
logoutall_url = reverse("durin_logoutall")
refresh_url = reverse("durin_refresh")

new_settings = durin_settings.defaults.copy()


class AuthTestCase(APITestCase):
    def setUp(self):
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

    def test_create_clients(self):
        self.assertEqual(Client.objects.count(), 1)
        Client.objects.all().delete()
        self.assertEqual(Client.objects.count(), 0)
        for name in self.client_names:
            Client.objects.create(name=name)
        self.assertEqual(Client.objects.count(), len(self.client_names))

    def test_create_tokens_for_users(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        self.test_create_clients()
        creds = self.creds.copy()
        creds2 = self.creds2.copy()
        for c in Client.objects.all():
            creds["client"] = c.name
            creds2["client"] = c.name
            # for user #1
            self.client.post(
                login_url,
                creds,
                format="json",
            )
            # for user #2
            self.client.post(
                login_url,
                creds2,
                format="json",
            )
        self.assertEqual(self.user.auth_token_set.count(), Client.objects.count())
        self.assertEqual(self.user2.auth_token_set.count(), Client.objects.count())
        self.assertTrue(all(t.token for t in AuthToken.objects.all()))

    def test_login_returns_serialized_token(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        response = self.client.post(
            login_url,
            self.creds,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(durin_settings.USER_SERIALIZER, None)
        self.assertIn("token", response.data)
        self.assertNotIn("user", response.data)
        self.assertNotIn(self.user.USERNAME_FIELD, response.data)

    def test_login_returns_serialized_token_and_username_field(self):
        new_settings["USER_SERIALIZER"] = UserSerializer
        with override_settings(REST_DURIN=new_settings):
            reload(views)
            self.assertEqual(AuthToken.objects.count(), 0)
            response = self.client.post(login_url, self.creds, format="json")
            self.assertEqual(new_settings["USER_SERIALIZER"], UserSerializer)
        reload(views)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        username_field = self.user.USERNAME_FIELD
        self.assertIn("user", response.data)
        self.assertIn(username_field, response.data["user"])

    def test_login_returns_configured_expiry_datetime_format(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        EXPIRY_DATETIME_FORMAT = "%H:%M %d/%m/%y"
        new_settings["EXPIRY_DATETIME_FORMAT"] = EXPIRY_DATETIME_FORMAT
        with override_settings(REST_DURIN=new_settings):
            reload(views)
            self.assertEqual(
                new_settings["EXPIRY_DATETIME_FORMAT"],
                EXPIRY_DATETIME_FORMAT,
            )
            response = self.client.post(login_url, self.creds, format="json")

        reload(views)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertNotIn("user", response.data)
        self.assertEqual(
            response.data["expiry"],
            DateTimeField(format=EXPIRY_DATETIME_FORMAT).to_representation(
                AuthToken.objects.first().expiry
            ),
        )

    def test_login_expiry_is_present(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        response = self.client.post(login_url, self.creds, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertIn("expiry", response.data)
        self.assertEqual(
            response.data["expiry"],
            DateTimeField().to_representation(AuthToken.objects.first().expiry),
        )

    def test_login_should_fail_if_no_client_in_request(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        self.creds.pop("client")
        response = self.client.post(login_url, self.creds, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "No client specified.")

    def test_expired_token_fails(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        instance = AuthToken.objects.create(
            self.user, self.authclient, delta_ttl=timedelta(seconds=0)
        )
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        response = self.client.get(root_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "The given token has expired."})

    def test_logout_deletes_keys(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        instance = AuthToken.objects.create(user=self.user, client=self.authclient)
        AuthToken.objects.create(user=self.user2, client=self.authclient)
        self.assertEqual(AuthToken.objects.count(), 2)

        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        self.client.post(logout_url, {}, format="json")
        self.assertEqual(
            AuthToken.objects.count(), 1, "other tokens should remain after logout"
        )

    def test_logout_all_deletes_keys(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        self.test_create_clients()
        for c in Client.objects.all():
            token = AuthToken.objects.create(user=self.user, client=c)
        self.assertEqual(AuthToken.objects.count(), len(self.client_names))

        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % token))
        self.client.post(logoutall_url, {}, format="json")
        self.assertEqual(AuthToken.objects.count(), 0)

    def test_logout_all_deletes_only_targets_keys(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        self.test_create_clients()
        for c in Client.objects.all():
            instance = AuthToken.objects.create(user=self.user, client=c)
            AuthToken.objects.create(user=self.user2, client=c)
        # 2 x len(self.client_names) tokens were created
        self.assertEqual(AuthToken.objects.count(), 2 * len(self.client_names))

        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        self.client.post(logoutall_url, {}, format="json")
        # now half of the tokens (for user #1) should have been deleted
        self.assertEqual(
            AuthToken.objects.count(),
            len(self.client_names),
            "tokens from other users should not be affected by logout all",
        )

    def test_update_token_key(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        self.assertEqual(Client.objects.count(), 1)
        instance = AuthToken.objects.create(self.user, self.authclient)
        rf = APIRequestFactory()
        request = rf.get("/")
        request.META = {"HTTP_AUTHORIZATION": "Token {}".format(instance.token)}
        (auth_user, auth_token) = TokenAuthentication().authenticate(request)
        self.assertEqual(
            instance.token,
            auth_token.token,
        )
        self.assertEqual(self.user, auth_user)

    def test_invalid_token_length_returns_401_code(self):
        invalid_token = "1" * (durin_settings.TOKEN_CHARACTER_LENGTH - 1)
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % invalid_token))
        response = self.client.get(root_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Invalid token."})

    def test_invalid_odd_length_token_returns_401_code(self):
        self.assertEqual(Client.objects.count(), 1)
        instance = AuthToken.objects.create(self.user, self.authclient)
        odd_length_token = instance.token + "1"
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % odd_length_token))
        response = self.client.get(root_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Invalid token."})

    def test_expiry_signals(self):
        self.signal_was_called = False

        def handler(sender, username, **kwargs):
            self.signal_was_called = True

        token_expired.connect(handler)

        instance = AuthToken.objects.create(
            user=self.user, client=self.authclient, delta_ttl=timedelta(seconds=0)
        )
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        self.client.get(root_url)

        self.assertTrue(self.signal_was_called)

    def test_invalid_auth_prefix_return_401(self):
        instance = AuthToken.objects.create(user=self.user, client=self.authclient)
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        ok_response = self.client.get(root_url)
        self.client.credentials(HTTP_AUTHORIZATION=("Baerer %s" % instance.token))
        failed_response = self.client.get(root_url)
        self.assertEqual(ok_response.status_code, 200)
        self.assertEqual(failed_response.status_code, 401)

    def test_invalid_auth_header_return_401(self):
        instance = AuthToken.objects.create(user=self.user, client=self.authclient)
        self.client.credentials(HTTP_AUTHORIZATION=("Token"))
        resp1 = self.client.get(root_url)
        self.assertEqual(resp1.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s typo" % instance.token))
        resp2 = self.client.get(root_url)
        self.assertEqual(resp2.status_code, 401)

    def test_login_same_token_existing_client(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        resp1 = self.client.post(login_url, self.creds, format="json")
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("token", resp1.data)
        self.assertEqual(AuthToken.objects.count(), 1)
        resp2 = self.client.post(login_url, self.creds, format="json")
        self.assertEqual(resp2.status_code, 200)
        self.assertIn("token", resp2.data)
        self.assertEqual(
            AuthToken.objects.count(),
            1,
            "should renew token, instead of creating new.",
        )
        self.assertEqual(
            resp1.data["expiry"],
            resp2.data["expiry"],
            "token expiry should be same after login",
        )
        self.assertEqual(
            resp1.data["token"],
            resp2.data["token"],
            "login should return existing token",
        )

    def test_login_renew_token_existing_client(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        new_settings["REFRESH_TOKEN_ON_LOGIN"] = True
        with override_settings(REST_DURIN=new_settings):
            reload(views)
            resp1 = self.client.post(login_url, self.creds, format="json")
            self.assertEqual(resp1.status_code, 200)
            self.assertIn("token", resp1.data)
            resp2 = self.client.post(login_url, self.creds, format="json")
            self.assertEqual(resp2.status_code, 200)
            self.assertIn("token", resp2.data)

        reload(views)
        self.assertEqual(
            AuthToken.objects.count(),
            1,
            "should renew token, instead of creating new.",
        )
        self.assertNotEqual(
            resp1.data["expiry"],
            resp2.data["expiry"],
            "token expiry should be renewed after login",
        )
        self.assertEqual(
            resp1.data["token"],
            resp2.data["token"],
            "token key must remain same",
        )

    def test_refresh_view_and_renewed_signal(self):
        self.signal_was_called = False

        def handler(sender, username, **kwargs):
            self.signal_was_called = True

        token_renewed.connect(handler)

        self.assertEqual(AuthToken.objects.count(), 0)
        instance = AuthToken.objects.create(user=self.user, client=self.authclient)
        self.assertEqual(AuthToken.objects.count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        resp = self.client.post(refresh_url, {}, format="json")
        self.assertEqual(
            AuthToken.objects.count(), 1, "refresh view should not create new token."
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("expiry", resp.data)
        self.assertNotEqual(resp.data["expiry"], instance.expiry)
        self.assertTrue(self.signal_was_called, "token_renewed signal was called.")

    def test_cached_api(self):
        self.assertEqual(AuthToken.objects.count(), 0)
        instance = AuthToken.objects.create(
            self.user, self.authclient, delta_ttl=timedelta(seconds=2)
        )
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % instance.token))
        resp1 = self.client.get(cached_auth_url)
        self.assertEqual(resp1.status_code, 200)
        time.sleep(2)
        self.assertTrue(instance.has_expired, "token expiry was set to 2 seconds.")
        resp2 = self.client.get(cached_auth_url)
        self.assertEqual(
            resp2.status_code,
            200,
            "token state was cached even though token has expired.",
        )
