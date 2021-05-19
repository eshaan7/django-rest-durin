"""
Durin provides a throttling class which make use of the
:class:`durin.models.Client` model it offers.

Usage is the same way as other
`DRF throttling classes <https://django-rest-framework.org/api-guide/throttling/>`__.

Example ``settings.py``::

        #...snip...
        REST_FRAMEWORK = {
            "DEFAULT_THROTTLE_CLASSES": ["durin.throttling.UserClientRateThrottle"],
            "DEFAULT_THROTTLE_RATES": {"user_per_client": "10/min"},
        }
        #...snip...

.. data:: "user_per_client"

    default ``scope`` for the :class:`UserClientRateThrottle` class.

    The rate defined here serves as the default rate incase the
    ``throttle_rate`` field on :class:`durin.models.Client` is ``null``.
"""

from django.core.exceptions import ValidationError as DjValidationError
from rest_framework.throttling import UserRateThrottle


class UserClientRateThrottle(UserRateThrottle):  # lgtm [py/missing-call-to-init]
    """
    Throttles requests by identifying the *authed* **user-client pair**.

    This is useful if you want to define different user throttle rates
    per :class:`durin.models.Client` instance.

    .. versionadded:: 0.2
    """

    #: Same as the default
    cache_format = "throttle_%(scope)s_%(ident)s"

    #: Scope for this throttle
    scope = "user_per_client"

    def __init__(self):
        # lgtm [py/missing-call-to-init]
        pass

    def allow_request(self, request, view):
        """
        The ``rate`` is set here because we need access to
        ``request`` object which is not available inside :py:meth:`~get_rate`.
        """
        if request.user.is_authenticated and hasattr(request, "_auth"):
            rate = request._auth.client.throttle_rate
            self.rate = rate if rate else self.get_rate()
        else:
            self.rate = self.get_rate()

        self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)

    def get_cache_key(self, request, view) -> str:
        if request.user.is_authenticated:
            # overwrite
            if hasattr(request, "_auth"):
                ident = self._get_user_client_ident(request)
            else:
                ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}

    def _get_user_client_ident(self, request) -> str:
        """
        Identify the user-client pair making the request.
        (assumes that ``request._auth`` is set, see :py:meth:`~get_cache_key`).
        """
        user_pk = request._auth.user_id
        client_pk = request._auth.client_id
        ident = "user-{0}.client-{1}".format(user_pk, client_pk)
        return ident

    @staticmethod
    def validate_client_throttle_rate(rate):
        """
        Used for validating the :attr:`throttle_rate` field
        on :class:`durin.models.Client`.

        *For internal use only.*
        """
        TIME_PERIODS_MAP = {"s": 1, "m": 60, "h": 3600, "d": 86400}

        try:
            num, period = rate.split("/")
            return int(num), TIME_PERIODS_MAP[period]
        except KeyError:
            raise DjValidationError("invalid period '{0}'.".format(period))
        except Exception as e:
            raise DjValidationError(e)
