from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from durin.auth import CachedTokenAuthentication, TokenAuthentication
from durin.throttling import UserClientRateThrottle


class RootView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("api root")


class CachedRootView(APIView):
    authentication_classes = (CachedTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("cached api root")


class ThrottledView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserClientRateThrottle,)

    def get(self, request):
        return Response("ThrottledView")
