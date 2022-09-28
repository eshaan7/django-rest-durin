import binascii
from os import urandom

import humanize
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from durin.settings import durin_settings
from durin.signals import token_renewed
from durin.throttling import UserClientRateThrottle

User = settings.AUTH_USER_MODEL


def _create_token_string() -> str:
    return binascii.hexlify(
        urandom(int(durin_settings.TOKEN_CHARACTER_LENGTH / 2))
    ).decode()


class Client(models.Model):
    """
    Identifier to represent any API client/browser that consumes your RESTful API.

    See ``example_project.models.ClientSettings``
    if you wish to extend this model per your convenience.
    """

    #: A unique identification name for the client.
    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        db_index=True,
        unique=True,
        help_text=_("A unique identification name for the client."),
    )

    #: Token Time To Live (TTL) in timedelta. Format: ``DAYS HH:MM:SS``.
    token_ttl = models.DurationField(
        null=False,
        default=durin_settings.DEFAULT_TOKEN_TTL,
        verbose_name=_("Token Time To Live (TTL)"),
        help_text=_(
            """
            Token Time To Live (TTL) in timedelta. Format: <code>DAYS HH:MM:SS</code>.
            """
        ),
    )

    #: Throttle rate for requests authed with this client.
    #:
    #: **Format**: ``number_of_requests/period``
    #: where period should be one of: *('s', 'm', 'h', 'd')*.
    #: (same format as DRF's throttle rates)
    #:
    #: **Example**: ``100/h`` implies 100 requests each hour.
    #:
    #: .. versionadded:: 0.2
    throttle_rate = models.CharField(
        max_length=64,
        default="",
        blank=True,
        verbose_name=_("Throttle rate for requests authed with this client"),
        help_text=_(
            """Follows the same format as DRF's throttle rates.
            Format: <em>'number_of_requests/period'</em>
            where period should be one of: ('s', 'm', 'h', 'd').
            Example: '100/h' implies 100 requests each hour.
            """
        ),
        validators=[UserClientRateThrottle.validate_client_throttle_rate],
    )

    def __str__(self):
        td = humanize.naturaldelta(self.token_ttl)
        rate = self.throttle_rate or "null"
        return "({0}: {1}, {2})".format(self.name, td, rate)


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
    """
    Token model with a unique constraint on ``User`` <-> ``Client`` relationship.
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "client"], name="unique token for user per client"
            )
        ]

    objects = AuthTokenManager()

    #: Token string
    token = models.CharField(
        max_length=durin_settings.TOKEN_CHARACTER_LENGTH,
        null=False,
        blank=False,
        db_index=True,
        unique=True,
        help_text=_("Token is auto-generated on save."),
    )
    #: :class:`~User` ForeignKey
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="auth_token_set",
        on_delete=models.CASCADE,
    )
    #: :class:`~Client` ForeignKey
    client = models.ForeignKey(
        Client,
        null=False,
        blank=False,
        related_name="auth_token_set",
        on_delete=models.CASCADE,
    )
    #: Created time
    created = models.DateTimeField(auto_now_add=True)
    #: Expiry time
    expiry = models.DateTimeField(null=False)

    def renew_token(self, request=None) -> "timezone.datetime":
        """
        Utility function to renew the token.

        Updates the :py:attr:`~expiry` attribute by ``Client.token_ttl``.
        """
        new_expiry = timezone.now() + self.client.token_ttl
        self.expiry = new_expiry
        self.save(update_fields=("expiry",))
        token_renewed.send(
            sender=self,
            request=request,
            new_expiry=new_expiry,
        )
        return new_expiry

    @property
    def expires_in(self) -> str:
        """
        Dynamic property that gives the :py:attr:`~expiry`
        attribute in human readable string format.

        Uses `humanize package <https://github.com/jmoiron/humanize>`__.
        """
        if self.expiry:
            td = self.expiry - self.created
            return humanize.naturaldelta(td)
        return "N/A"

    @property
    def has_expired(self) -> bool:
        """
        Dynamic property that returns ``True`` if token has expired,
        otherwise ``False``.
        """
        return timezone.now() > self.expiry

    def __repr__(self) -> str:
        return "({0}, {1}/{2})".format(
            self.token, self.user.get_username(), self.client.name
        )

    def __str__(self) -> str:
        return self.token
