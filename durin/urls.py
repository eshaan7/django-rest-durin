from django.conf.urls import url

from durin import views

urlpatterns = [
    url(r"login/", views.LoginView.as_view(), name="durin_login"),
    url(r"refresh/", views.RefreshView.as_view(), name="durin_refresh"),
    url(r"logout/", views.LogoutView.as_view(), name="durin_logout"),
    url(r"logoutall/", views.LogoutAllView.as_view(), name="durin_logoutall"),
]
