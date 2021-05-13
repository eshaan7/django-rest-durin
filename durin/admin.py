from django.contrib import admin

from durin import models


class ClientSetttingsInlineAdmin(admin.StackedInline):
    """
    Django's StackedInline for :class:`ClientSettings` model.
    """

    model = models.ClientSettings


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    """Django's ModelAdmin for AuthToken.\n
    In most cases, you would want to override this to make
    ``AuthTokenAdmin.raw_id_fields = ("user",)``
    """

    exclude = ("token", "expiry")
    list_display = (
        "token",
        "client_name",
        "user",
        "created",
        "expires_in",
    )
    list_filter = ("client__name", "user")

    fieldsets = [
        (
            "API Auth Token",
            {
                "fields": ("user", "client"),
                "description": """
                    <h3>Token will be auto-generated on save.</h3>
                    <h3>Token will carry the same expiry as the
                     selected client's token TTL.</h3>
                """,
            },
        ),
    ]

    def client_name(self, obj):
        return obj.client.name

    def save_model(self, request, obj, form, change):
        if not change:
            created_obj = models.AuthToken.objects.create(obj.user, obj.client)
            obj.pk = created_obj.pk
            obj.token = created_obj.token
            obj.expiry = created_obj.expiry
        else:
            super(AuthTokenAdmin, self).save_model(request, obj, form, change)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Django's ModelAdmin for :class:`Client` model.
    """

    inlines = [
        ClientSetttingsInlineAdmin,
    ]

    list_display = ("id", "name", "token_ttl", "settings")
