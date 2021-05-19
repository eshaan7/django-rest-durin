from durin import permissions

TEST_CLIENT_NAME = "testpermissionsclient"


class CustomAllowSpecificClients(permissions.AllowSpecificClients):

    allowed_clients_name = (TEST_CLIENT_NAME,)


class CustomDisallowSpecificClients(permissions.DisallowSpecificClients):

    disallowed_clients_name = (TEST_CLIENT_NAME,)
