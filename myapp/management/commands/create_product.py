from django.core.management.base import BaseCommand
from myapp.models import Product
from decimal import Decimal
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils import lorem_ipsum


class Command(BaseCommand):
    help = "Create a new product"

    def handle(self, *args, **kwargs):
        name = get_random_string(length=10,
                                 allowed_chars='abcdefghijklmnopqrstuvwxyz').capitalize()
        description = lorem_ipsum.words(15, common=False).capitalize()
        price = Decimal(get_random_string(length=2, allowed_chars='0123456789')).quantize(Decimal('.01'))
        quantity = int(get_random_string(length=3, allowed_chars='123456789'))
        added_date = timezone.now().date()
        print(added_date)
        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            added_date=added_date,
        )
        product.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product}'))
