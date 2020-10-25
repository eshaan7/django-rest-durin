import django.dispatch

token_expired = django.dispatch.Signal(providing_args=["username", "source"])
"""
When a token is expired and deleted.

        providing_args=["username", "source"]
"""

token_renewed = django.dispatch.Signal(
    providing_args=["username", "token_id", "expiry"]
)
"""
When a token is renewed by either :class:`durin.views.LoginView`
or :class:`durin.views.RefreshView`.

        providing_args=["username", "token_id", "expiry"]
"""
