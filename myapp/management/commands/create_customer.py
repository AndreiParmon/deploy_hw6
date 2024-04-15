from django.core.management.base import BaseCommand
from myapp.models import Customer
from django.utils.crypto import get_random_string
from django.utils import timezone


class Command(BaseCommand):
    help = "Create a new customer"

    def handle(self, *args, **kwargs):
        name = get_random_string(length=7,
                                 allowed_chars='abcdefghijklmnopqrstuvwxyz').capitalize()
        email = f"{name.lower()}@gmail.com"
        phone_number = get_random_string(length=12, allowed_chars='0123456789')
        address = get_random_string(15)
        registration_date = timezone.now().date()
        customer = Customer(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            registration_date=registration_date,
        )
        customer.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created customer: {customer}'))
