from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from durin.auth import CachedTokenAuthentication
from durin.throttling import UserClientRateThrottle

from .permissions import CustomAllowSpecificClients, CustomDisallowSpecificClients


class RootView(APIView):
    def get(self, request):
        return Response("api root")


class CachedRootView(APIView):
    authentication_classes = (CachedTokenAuthentication,)

    def get(self, request):
        return Response("cached api root")


class ThrottledView(APIView):
    throttle_classes = (UserClientRateThrottle,)

    def get(self, request):
        return Response("ThrottledView")


class OnlyWebClientView(APIView):
    """
    Only accessible to TEST_CLIENT_NAME
    """

    permission_classes = (CustomAllowSpecificClients, IsAuthenticated)

    def get(self, request):
        return Response("OnlyWebClientView")


class NoWebClientView(APIView):
    """
    Not accessible to TEST_CLIENT_NAME
    """

    permission_classes = (CustomDisallowSpecificClients, IsAuthenticated)

    def get(self, request):
        return Response("NoWebClientView")
