from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from .views import CachedRootView, RootView, ThrottledView

urlpatterns = [
    path("", RedirectView.as_view(url="admin/", permanent=False)),
    path("admin/", admin.site.urls, name="admin"),
    re_path(r"^api/", include("durin.urls")),
    re_path(r"^api/$", RootView.as_view(), name="api-root"),
    re_path(r"^api/cached$", CachedRootView.as_view(), name="cached-auth-api"),
    re_path(r"^api/throttled$", ThrottledView.as_view(), name="throttled-api"),
]
