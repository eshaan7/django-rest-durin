"""
Durin provides two permission classes which make use of the :class:`durin.models.Client`
model it offers.

You can use these the same way as other
`DRF permissions <https://www.django-rest-framework.org/api-guide/permissions/>`__ or
activate them on all your views by adding
them to ``REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]``
under your app's ``settings.py``
"""

from rest_framework.permissions import BasePermission


class AllowSpecificClients(BasePermission):
    """
    Allows access to only specific clients.\n
    Should be used along with :doc:`auth`.
    """

    #: Include names of allowed clients to ``allowed_clients_name``.
    allowed_clients_name = ()

    def has_permission(self, request, view):
        if not hasattr(request, "_auth"):
            return False
        return request._auth.client.name in self.allowed_clients_name


class DisallowSpecificClients(BasePermission):
    """
    Restrict specific clients from making requests.\n
    Should be used along with :doc:`auth`.
    """

    #: Include names of disallowed clients to ``disallowed_clients_name``.
    disallowed_clients_name = ()

    def has_permission(self, request, view):
        if not hasattr(request, "_auth"):
            return False
        return request._auth.client.name not in self.disallowed_clients_name
