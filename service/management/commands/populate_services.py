from django.core.management import BaseCommand

from service.models import Service


from managepro.constants import SERVICES_DATA


class Command(BaseCommand):
    help = "Populate the Service model with initial data"

    def handle(self):
        for service in SERVICES_DATA:
            obj, created = Service.objects.get_or_create(
                name=service["name"], image_url=service["imageUrl"], domain=service["link"])

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Added {service['name']}"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"{service['name']} already exists"))
