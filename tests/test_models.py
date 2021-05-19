from django.core.exceptions import ValidationError as DjValidationError
from django.test import TestCase

from durin.models import Client


class ClientTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client_names = ["web", "mobile", "cli"]
        return super().setUpClass()

    def test_create_clients(self):
        Client.objects.all().delete()
        self.assertEqual(Client.objects.count(), 0)
        for name in self.client_names:
            Client.objects.create(name=name)
        self.assertEqual(Client.objects.count(), len(self.client_names))

    def test_throttle_rate_validation_ok(self):
        testclient = Client.objects.create(
            name="test_throttle_rate_validation", throttle_rate="2/m"
        )
        testclient.full_clean()

        self.assertIsNotNone(testclient.pk)
        self.assertIsNotNone(testclient.token_ttl)
        self.assertIsNotNone(testclient.throttle_rate)

    def test_throttle_rate_validation_raises_exc(self):

        with self.assertRaises(DjValidationError):
            testclient1 = Client.objects.create(
                name="testclient1", throttle_rate="blahblah"
            )
            testclient1.full_clean()
            testclient1.delete()

        with self.assertRaises(DjValidationError):
            testclient2 = Client.objects.create(
                name="testclient2",
                throttle_rate="2/minute",
            )
            testclient2.full_clean()
            testclient2.delete()
