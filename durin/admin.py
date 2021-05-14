from django.contrib import admin

from durin import models


class ClientSettingsInlineAdmin(admin.StackedInline):
    """
    Django's StackedInline for :class:`ClientSettings` model.
    """

    model = models.ClientSettings


class UserClientInlineAdmin(admin.TabularInline):
    model = models.UserClient
    list_select_related = True
    fields = ("user", "client")
    extra = 1


@admin.register(models.UserClient)
class UserClientAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ("user", "client", "authtoken")


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    """Django's ModelAdmin for AuthToken.\n
    In most cases, you would want to override this to make
    ``AuthTokenAdmin.raw_id_fields = ("user",)``
    """

    list_select_related = True

    list_display = (
        "token",
        "userclient",
        "created",
        "expires_in",
    )
    list_filter = ("userclient__client", "userclient__user")

    readonly_fields = ("token", "expiry", "created", "expires_in")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return [
                (
                    "API Auth Token",
                    {
                        "fields": ("userclient",),
                        "description": """
                    <h3>Token will be auto-generated on save.</h3>
                    <h3>Token will carry the same expiry as the
                     selected client's token TTL.</h3>
                """,
                    },
                ),
            ]
        else:
            return super().get_fieldsets(request, obj)

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            created_obj = models.AuthToken.objects.create(userclient=obj.userclient)
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

    inlines = [ClientSettingsInlineAdmin, UserClientInlineAdmin]

    list_display = ("id", "name", "token_ttl", "settings")
