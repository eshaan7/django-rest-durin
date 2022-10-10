from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _

from durin.serializers import ClientSerializer


class Command(BaseCommand):
    help = "Creates a new client with the given values."

    def add_arguments(self, parser):
        parser.add_argument(
            "name", type=str, help=_("A unique identification name for the client.")
        )
        parser.add_argument(
            "--token-ttl",
            type=str,
            default="",
            help=_(
                "Token Time To Live (TTL) in timedelta. "
                "Format: <code>DAYS HH:MM:SS</code>."
            ),
        )
        parser.add_argument(
            "--throttle-rate",
            type=str,
            default="",
            help=_(
                "Follows the same format as DRF's throttle rates. "
                "Format: <em>'number_of_requests/period'</em> "
                "where period should be one of: ('s', 'm', 'h', 'd'). "
                "Example: '100/h' implies 100 requests each hour."
            ),
        )

    def handle(self, *args, **options):
        client = ClientSerializer(
            data={
                "name": options["name"],
                "token_ttl": options["token_ttl"],
                "throttle_rate": options["throttle_rate"],
            }
        )
        if client.is_valid():
            client.save()
            self.stdout.write(
                self.style.SUCCESS("Client {} created!".format(client.data.get("name")))
            )
            return
        raise CommandError(
            (
                "Can't create client!\n"
                + "\n".join(
                    (
                        "{field}: {errors}".format(field=field, errors=" ".join(errors))
                        for field, errors in client.errors.items()
                    )
                )
            )
        )
