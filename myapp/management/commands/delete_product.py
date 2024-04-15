from django.core.management.base import BaseCommand
from myapp.models import Product


class Command(BaseCommand):
    help = "Delete a product"

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='Product ID')

    def handle(self, *args, **kwargs):
        pk = kwargs.get('pk')
        product = Product.objects.filter(pk=pk).first()
        if product is not None:
            product.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted product: {product}'))
