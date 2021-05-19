from django.contrib import admin

from durin.models import Client

from .models import ClientSettings


class ClientSettingsInlineAdmin(admin.StackedInline):
    """
    Django's StackedInline for :class:`ClientSettings` model.
    """

    model = ClientSettings

    list_select_related = True
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    """
    Django's ModelAdmin for :class:`Client` model.
    """

    inlines = [
        ClientSettingsInlineAdmin,
    ]

    list_display = (
        "id",
        "name",
        "token_ttl",
        "throttle_rate",
    )


# Unregister default admin view
admin.site.unregister(Client)
admin.site.register(Client, ClientAdmin)
