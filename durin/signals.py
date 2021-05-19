import django.dispatch

token_expired = django.dispatch.Signal()
"""
When a token is expired and deleted.

        providing_args=["username", "source"]
"""

token_renewed = django.dispatch.Signal()
"""
When a token is renewed by either :class:`durin.views.LoginView`
or :class:`durin.views.RefreshView`.

        providing_args=["request", "new_expiry"]
"""
