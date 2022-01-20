from django.urls import re_path

from durin import views

urlpatterns = [
    re_path(r"login/", views.LoginView.as_view(), name="durin_login"),
    re_path(r"refresh/", views.RefreshView.as_view(), name="durin_refresh"),
    re_path(r"logout/", views.LogoutView.as_view(), name="durin_logout"),
    re_path(r"logoutall/", views.LogoutAllView.as_view(), name="durin_logoutall"),
]
