from django.urls import include, re_path

from .views import CachedRootView, RootView

urlpatterns = [
    re_path(r"^api/", include("durin.urls")),
    re_path(r"^api/$", RootView.as_view(), name="api-root"),
    re_path(r"^api/cached$", CachedRootView.as_view(), name="cached-auth-api"),
]
