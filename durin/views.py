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
    def get_token_client(request):
        client_name = request.data.get("client", None)
        if not client_name:
            raise ParseError("No client specified.", status.HTTP_400_BAD_REQUEST)
        return Client.objects.get(name=client_name)

    def format_expiry_datetime(self, expiry):
        datetime_format = durin_settings.EXPIRY_DATETIME_FORMAT
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, instance):
        UserSerializer = durin_settings.USER_SERIALIZER

        data = {
            "expiry": self.format_expiry_datetime(instance.expiry),
            "token": instance.token,
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(request.user, context=self.get_context()).data
        return data

    @staticmethod
    def get_new_token(user, client):
        return AuthToken.objects.create(user, client)

    def post(self, request, format=None):
        request.user = self.validate_and_return_user(request)
        client = self.get_token_client(request)
        try:
            # a token for this user and client already exists,
            # so we can return the same one by renewing it's expiry
            instance = AuthToken.objects.get(user=request.user, client=client)
            instance.renew_token(renewed_by=self.__class__)
        except ObjectDoesNotExist:
            # create new token
            instance = self.get_new_token(request.user, client)

        user_logged_in.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        data = self.get_post_response_data(request, instance)
        return Response(data)


class RefreshView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        auth_token = request._auth
        new_expiry = auth_token.renew_token(renewed_by=self.__class__)
        return Response({"expiry": new_expiry}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    """
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)
