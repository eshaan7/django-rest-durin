from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from durin.auth import CachedTokenAuthentication, TokenAuthentication
from durin.throttling import UserClientRateThrottle

from .permissions import CustomAllowSpecificClients, CustomDisallowSpecificClients


class _BaseAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class RootView(_BaseAPIView):
    def get(self, request):
        return Response("api root")


class CachedRootView(_BaseAPIView):
    authentication_classes = (CachedTokenAuthentication,)

    def get(self, request):
        return Response("cached api root")


class ThrottledView(_BaseAPIView):
    throttle_classes = (UserClientRateThrottle,)

    def get(self, request):
        return Response("ThrottledView")


class RestrictedAllowView(_BaseAPIView):
    """
    Only accessible to TEST_CLIENT_NAME
    """

    permission_classes = (IsAuthenticated, CustomAllowSpecificClients)

    def get(self, request):
        return Response("RestrictedAllowView")


class RestrictedDisallowView(_BaseAPIView):
    """
    Not accessible to TEST_CLIENT_NAME
    """

    permission_classes = (IsAuthenticated, CustomDisallowSpecificClients)

    def get(self, request):
        return Response("RestrictedDisallowView")
