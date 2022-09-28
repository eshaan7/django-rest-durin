from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from durin.models import AuthToken
from durin.settings import durin_settings
from durin.signals import token_expired

# try to import memoize
memoize = None

try:
    from cache_memoize import cache_memoize as memoize
except ImportError:
    pass


class TokenAuthentication(BaseAuthentication):
    """
    This authentication scheme uses Durin's
    :class:`durin.models.AuthToken` for authentication.

    Similar to `DRF's authentication system
    <http://www.django-rest-framework.org/api-guide/authentication/>`__,
    it overrides it a bit to
    accomodate that tokens can be expired.

    If successful,

    - ``request.user`` will be a django ``User`` instance
    - ``request.auth`` will be an ``AuthToken`` instance
    """

    model = AuthToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = durin_settings.AUTH_HEADER_PREFIX.encode()

        if not auth or auth[0].lower() != prefix.lower():
            return None
        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = _("Invalid token header. " "Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    @classmethod
    def authenticate_credentials(cls, token):
        """
        Verify that the given token exists in the database
        """
        token_str = token.decode("utf-8")
        try:
            # read settings
            to_select = durin_settings.AUTHTOKEN_SELECT_RELATED_LIST

            # get AuthToken object
            if isinstance(to_select, list):
                auth_token = AuthToken.objects.select_related(*to_select).get(
                    token=token_str
                )
            else:
                auth_token = AuthToken.objects.get(token=token_str)

            # validate token
            if cls._cleanup_token(auth_token):
                e = _("The given token has expired.")
                raise exceptions.AuthenticationFailed(e)
            return cls.validate_user(auth_token)
        except exceptions.AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(e)
        except Exception:
            msg = _("Invalid token.")
            raise exceptions.AuthenticationFailed(msg)

    @staticmethod
    def validate_user(auth_token: AuthToken):
        if not auth_token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))
        return (auth_token.user, auth_token)

    def authenticate_header(self, request):
        return durin_settings.AUTH_HEADER_PREFIX

    @classmethod
    def _cleanup_token(cls, auth_token: AuthToken):
        if auth_token.expiry is not None:
            if auth_token.has_expired:
                username = auth_token.user.get_username()
                auth_token.delete()
                token_expired.send(sender=cls, username=username, source="auth_token")
                return True
        return False


# if memoize is available, create another token authentication class
# which uses django-memoize for caching
if memoize:

    class CachedTokenAuthentication(TokenAuthentication):
        """
        Similar to ``TokenAuthentication`` but uses
        `django-cache-memoize <https://github.com/peterbe/django-cache-memoize>`__
        as cache backend for faster lookups.

        The cache timeout is configurable by setting the
        ``REST_DURIN["TOKEN_CACHE_TIMEOUT"]`` under your app's ``settings.py``.

        **How To Enable:**

        1. Install django-cache-memoize

        .. parsed-literal::
            pip install django-cache-memoize

        2. Then you need to use ``CachedTokenAuthentication``
           instead of ``TokenAuthentication``.
        """

        @classmethod
        @memoize(timeout=int(durin_settings.TOKEN_CACHE_TIMEOUT))
        def authenticate_credentials(cls, token):
            return super().authenticate_credentials(token)

        def __repr__(self):
            return self.__class__.__name__
