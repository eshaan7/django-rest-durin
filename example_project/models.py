from django.db import models


class ClientSettings(models.Model):
    """
    It is recommended to create a model like this
    (and not subclass :py:class:`durin.models.Client`)
    if you wish to add extra fields for storing any
    configuration or settings against ``Client`` instances.

    Reverse lookup: ``Client.settings``.
    """

    #: `OneToOneField
    #: <https://docs.djangoproject.com/en/3.2/topics/db/examples/one_to_one/>`__
    #: with :py:class:`~Client` with ``on_delete=models.CASCADE``.
    client = models.OneToOneField(
        "durin.Client",
        blank=False,
        related_name="settings",
        on_delete=models.CASCADE,
    )

    description = models.TextField()

    def __str__(self):
        return "ClientSettings(<{0}>)".format(self.client.name)
