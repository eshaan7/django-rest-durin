from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from .views import (
    CachedRootView,
    NoWebClientView,
    OnlyWebClientView,
    RootView,
    ThrottledView,
)

urlpatterns = [
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("admin/", admin.site.urls, name="admin"),
    re_path(r"^api/", include("durin.urls")),
    re_path(r"^api/$", RootView.as_view(), name="api-root"),
    re_path(r"^api/cached$", CachedRootView.as_view(), name="cached-auth-api"),
    re_path(r"^api/throttled$", ThrottledView.as_view(), name="throttled-api"),
    re_path(
        r"^api/onlywebclient$",
        OnlyWebClientView.as_view(),
        name="onlywebclient-api",
    ),
    re_path(
        r"^api/nowebclient$",
        NoWebClientView.as_view(),
        name="nowebclient-api",
    ),
]
