import django.dispatch

token_expired = django.dispatch.Signal(providing_args=["username", "source"])

token_renewed = django.dispatch.Signal(
    providing_args=["username", "token_id", "expiry"]
)
