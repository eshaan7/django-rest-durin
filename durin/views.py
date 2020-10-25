from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.views import APIView

from durin.auth import TokenAuthentication
from durin.models import AuthToken, Client
from durin.settings import durin_settings


class LoginView(APIView):
    """Durin's Login View.\n
    This view will return a JSON response when valid ``username``, ``password`` and
    if not overwritten ``client`` fields are POSTed to the view using
    form data or JSON.

    It uses the default serializer provided by
    Django-Rest-Framework (``rest_framework.authtoken.serializers.AuthTokenSerializer``)
    to validate the user credentials.

    It is possible to customize LoginView behaviour by overriding the following
    helper methods:
    """

    authentication_classes = []
    permission_classes = []

    def get_context(self):
        """
        to change the context passed to the ``UserSerializer``.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    @staticmethod
    def validate_and_return_user(request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user"]

    @staticmethod
    def get_client_obj(request) -> "Client":
        """
        To get and return the associated :class:`durin.models.Client` object.
        """
        client_name = request.data.get("client", None)
        if not client_name:
            raise ParseError("No client specified.", status.HTTP_400_BAD_REQUEST)
        return Client.objects.get(name=client_name)

    @classmethod
    def get_token_obj(cls, request, client: "Client") -> "AuthToken":
        """
        Flow used to return the :class:`durin.models.AuthToken` object.
        """
        try:
            # a token for this user and client already exists, so we can just return it
            token = AuthToken.objects.get(user=request.user, client=client)
            if durin_settings.REFRESH_TOKEN_ON_LOGIN:
                cls.renew_token(token)
        except ObjectDoesNotExist:
            # create new token
            token = AuthToken.objects.create(request.user, client)

        return token

    @classmethod
    def renew_token(cls, token_obj: "AuthToken") -> None:
        """
        How to renew the token instance in case
        ``settings.REFRESH_TOKEN_ON_LOGIN`` is set to ``True``.
        """
        token_obj.renew_token(renewed_by=cls)

    @staticmethod
    def format_expiry_datetime(expiry):
        """
        To format the expiry ``datetime`` object at your convenience.
        """
        datetime_format = durin_settings.EXPIRY_DATETIME_FORMAT
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_user_serializer_class(self):
        """
        To change the class used for serializing the user.
        """
        return durin_settings.USER_SERIALIZER

    def get_post_response_data(self, request, token_obj: "AuthToken"):
        """
        Override this to return a fully customized payload.
        """
        UserSerializer = self.get_user_serializer_class()
        data = {
            "expiry": self.format_expiry_datetime(token_obj.expiry),
            "token": token_obj.token,
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(request.user, context=self.get_context()).data
        return data

    def post(self, request, *args, **kwargs):
        request.user = self.validate_and_return_user(request)
        client = self.get_client_obj(request)
        token_obj = self.get_token_obj(request, client)
        user_logged_in.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        data = self.get_post_response_data(request, token_obj)
        return Response(data)


class RefreshView(APIView):
    """Durin's Refresh View\n
    This view accepts only a post request with an empty body.
    It responds to Durin Token Authentication. On a successful request,

    1. The given token's expiry is extended by it's associated
       :py:attr:`durin.models.Client.token_ttl`
       duration and a JSON object will be returned containing a single ``expiry``
       key as the new timestamp for when the token expires.

    2. :meth:`durin.signals.token_renewed` is called.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def format_expiry_datetime(expiry):
        """
        To format the expiry ``datetime`` object at your convenience.
        """
        datetime_format = durin_settings.EXPIRY_DATETIME_FORMAT
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def post(self, request, *args, **kwargs):
        auth_token = request._auth
        new_expiry = auth_token.renew_token(renewed_by=self.__class__)
        new_expiry_repr = self.format_expiry_datetime(new_expiry)
        return Response({"expiry": new_expiry_repr}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Durin's Logout View.\n
    This view accepts only a post request with an empty body.
    It responds to Durin Token Authentication. On a successful request,

    1. The token used to authenticate is deleted from
       the database and can no longer be used to authenticate.

    2. :meth:`django.contrib.auth.signals.user_logged_out` is called.

    :returns: 204 (No content)
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    """Durin's LogoutAllView.\n
    This view accepts only a post request with an empty body. It responds to Durin Token
    Authentication.
    On a successful request,

    1. The token used to authenticate, and **all other tokens**
       registered to the same ``User`` account, are deleted from the
       system and can no longer be used to authenticate.

    2. :meth:`django.contrib.auth.signals.user_logged_out` is called.

    :returns: 204 (No content)
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)
