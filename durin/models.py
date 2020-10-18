import binascii
from os import urandom

import humanize
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from durin.settings import durin_settings
from durin.signals import token_renewed

User = settings.AUTH_USER_MODEL


def _create_token_string() -> str:
    return binascii.hexlify(
        urandom(int(durin_settings.TOKEN_CHARACTER_LENGTH / 2))
    ).decode()


class Client(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        db_index=True,
        unique=True,
        help_text=_("A unique identification name for the client."),
    )
    token_ttl = models.DurationField(
        null=False,
        default=durin_settings.DEFAULT_TOKEN_TTL,
        verbose_name=_("Token Time To Live (TTL)"),
        help_text=_(
            """
            Token Time To Live (TTL) in timedelta. Format: <em>DAYS HH:MM:SS</em>.
            """
        ),
    )

    def __str__(self):
        td = humanize.naturaldelta(self.token_ttl)
        return "({0}, {1})".format(self.name, td)


class AuthTokenManager(models.Manager):
    def create(self, user, client, delta_ttl=None):
        token = _create_token_string()

        if delta_ttl is not None:
            expiry = timezone.now() + delta_ttl
        else:
            expiry = timezone.now() + client.token_ttl

        instance = super(AuthTokenManager, self).create(
            token=token, user=user, client=client, expiry=expiry
        )
        return instance


class AuthToken(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "client"], name="unique token for user per client"
            )
        ]

    objects = AuthTokenManager()

    token = models.CharField(
        max_length=durin_settings.TOKEN_CHARACTER_LENGTH,
        null=False,
        blank=False,
        db_index=True,
        unique=True,
        help_text=_("Token is auto-generated on save."),
    )
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="auth_token_set",
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        Client,
        null=False,
        blank=False,
        related_name="auth_token_set",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=False)

    def renew_token(self, renewed_by):
        new_expiry = timezone.now() + self.client.token_ttl
        self.expiry = new_expiry
        self.save(update_fields=("expiry",))
        token_renewed.send(
            sender=renewed_by,
            username=self.user.get_username(),
            token_id=self.pk,
            expiry=new_expiry,
        )
        return new_expiry

    @property
    def expires_in(self) -> str:
        if self.expiry:
            td = self.expiry - self.created
            return humanize.naturaldelta(td)
        else:
            return "N/A"

    @property
    def has_expired(self) -> bool:
        return timezone.now() > self.expiry

    def __repr__(self) -> str:
        return "({0}, {1}/{2})".format(
            self.token, self.user.get_username(), self.client.name
        )

    def __str__(self) -> str:
        return self.token
