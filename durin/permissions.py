from rest_framework.permissions import BasePermission


class AllowSpecificClients(BasePermission):
    """
    Allows access to only specific clients.
    Should be used along with `durin.auth.TokenAuthentication`.
    """

    allowed_clients_name = ("web",)

    def has_permission(self, request, view):
        if not hasattr(request, "_auth"):
            return False
        return request._auth.client.name in self.allowed_clients_name


class DisallowSpecificClients(BasePermission):
    """
    restrict specific clients from making requests.
    Should be used along with `durin.auth.TokenAuthentication`.
    """

    disallowed_clients_name = ()

    def has_permission(self, request, view):
        if not hasattr(request, "_auth"):
            return False
        return request._auth.client.name not in self.disallowed_clients_name
