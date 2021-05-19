"""
Durin provides two *abstract* permission classes which
make use of the :class:`durin.models.Client`
model it offers.

You will need to subclass them and modify the
``allowed_clients_name`` or ``disallowed_clients_name`` property per your wish.

Then you may use them the same way as other
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
        if not request.auth:
            return False
        return request.auth.client.name in self.allowed_clients_name


class DisallowSpecificClients(BasePermission):
    """
    Restrict specific clients from making requests.\n
    Should be used along with :doc:`auth`.
    """

    #: Include names of disallowed clients to ``disallowed_clients_name``.
    disallowed_clients_name = ()

    def has_permission(self, request, view):
        if not request.auth:
            return False
        return request.auth.client.name not in self.disallowed_clients_name
