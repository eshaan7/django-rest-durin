from io import StringIO

from django.core import management
from django.core.management import CommandError
from django.test import TestCase

from durin.models import Client


class ClientCommandTestCase(TestCase):
    @staticmethod
    def call_command(*args, **kwargs):
        out = StringIO()
        management.call_command(
            "create_client", *args, stdout=out, stderr=StringIO(), **kwargs
        )
        return out.getvalue()

    def test__create_client__valid_name(self):
        client_name = "web"
        self.assertEqual(Client.objects.count(), 0)

        out = self.call_command(client_name)

        self.assertEqual(out, "Client {} created!\n".format(client_name))
        self.assertEqual(Client.objects.count(), 1)

    def test__create_client__valid_data(self):
        client_name = "web"
        ttl = "14 00:00"
        throttle_rate = "1/s"
        self.assertEqual(Client.objects.count(), 0)

        out = self.call_command(client_name, token_ttl=ttl, throttle_rate=throttle_rate)

        self.assertEqual(out, "Client {} created!\n".format(client_name))
        self.assertEqual(Client.objects.count(), 1)

    def test__create_client__name_not_set_raises_exc(self):
        with self.assertRaises(CommandError):
            self.call_command()

    def test_create_client__blank_name_raises_exc(self):
        with self.assertRaisesMessage(
            CommandError, "name: This field may not be blank."
        ):
            self.call_command("")

    def test_create_client__invalid_ttl_raises_exc(self):
        with self.assertRaisesMessage(
            CommandError,
            (
                "token_ttl: Duration has wrong format. "
                "Use one of these formats instead: [DD] [HH:[MM:]]ss[.uuuuuu]."
            ),
        ):
            self.call_command("web", token_ttl="invalid")
