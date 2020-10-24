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
    """Durin's Login View.
    It accepts user credentials (username and password) validates same
    and returns token key, expiry and
    user fields present in `durin.settings.USER_SERIALIZER`.
    """

    authentication_classes = []
    permission_classes = []

    def get_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    @staticmethod
    def validate_and_return_user(request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user"]

    @staticmethod
    def get_client_obj(request) -> "Client":
        client_name = request.data.get("client", None)
        if not client_name:
            raise ParseError("No client specified.", status.HTTP_400_BAD_REQUEST)
        return Client.objects.get(name=client_name)

    @staticmethod
    def format_expiry_datetime(expiry):
        datetime_format = durin_settings.EXPIRY_DATETIME_FORMAT
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token_obj: "AuthToken"):
        UserSerializer = durin_settings.USER_SERIALIZER

        data = {
            "expiry": self.format_expiry_datetime(token_obj.expiry),
            "token": token_obj.token,
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(request.user, context=self.get_context()).data
        return data

    @classmethod
    def renew_token(cls, token_obj: "AuthToken"):
        token_obj.renew_token(renewed_by=cls)

    @classmethod
    def get_token_obj(cls, request, client: "Client") -> "AuthToken":
        try:
            # a token for this user and client already exists, so we can just return it
            token = AuthToken.objects.get(user=request.user, client=client)
            if durin_settings.REFRESH_TOKEN_ON_LOGIN:
                cls.renew_token(token)
        except ObjectDoesNotExist:
            # create new token
            token = AuthToken.objects.create(request.user, client)

        return token

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
    """Durin's Refresh View
    Refreshes the token present in request header and returns new expiry
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def format_expiry_datetime(expiry):
        datetime_format = durin_settings.EXPIRY_DATETIME_FORMAT
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def post(self, request, *args, **kwargs):
        auth_token = request._auth
        new_expiry = auth_token.renew_token(renewed_by=self.__class__)
        new_expiry_repr = self.format_expiry_datetime(new_expiry)
        return Response({"expiry": new_expiry_repr}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Durin's Logout View.
    Delete's the token present in request header.

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
    """Durin's LogoutAllView
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)
