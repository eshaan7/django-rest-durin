***************************************
Authentication (``durin.auth``)
***************************************

Durin provides one ``TokenAuthentication`` backend and
``CachedTokenAuthentication`` which uses memoization for faster look ups.

TokenAuthentication
--------------------------

.. autoclass:: durin.auth.TokenAuthentication
   :show-inheritance:

Durin tokens should be generated using the provided views.
Any ``APIView`` or ``ViewSet`` can be accessed using these tokens by adding ``TokenAuthentication``
to the View's ``authentication_classes``.
To authenticate, the ``Authorization`` header should be set on the request, like::

    Authorization: Token adee69d0e4bbdc6e4m9836F45E23A325

**Note**: The prefix can be configured by setting the ``REST_DURIN["AUTH_HEADER_PREFIX"]`` (`ref <settings.html#AUTH_HEADER_PREFIX>`__).

**Example Usage**::

    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response
    from rest_framework.views import APIView

    from durin.auth import TokenAuthentication

    class ExampleView(APIView):
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        def get(self, request, *args, **kwargs):
            content = {
                'foo': 'bar'
            }
            return Response(content)

Tokens expire after a preset time. See `settings.DEFAULT_TOKEN_TTL <settings.html#DEFAULT_TOKEN_TTL>`__.

--------------------------

CachedTokenAuthentication
--------------------------

.. autoclass:: durin.auth.CachedTokenAuthentication
   :show-inheritance:

--------------------------

Global usage on all views
--------------------------

You can activate Durin's :class:`durin.auth.TokenAuthentication` or 
:class:`durin.auth.CachedTokenAuthentication` on all your views by adding it to 
``REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]`` under your app's ``settings.py``. 
Make sure to not use both of these together.

.. Warning:: If you use `Token Authentication` in production you must ensure that your API is only available over HTTPS (SSL).
