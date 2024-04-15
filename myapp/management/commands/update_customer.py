from django.core.management.base import BaseCommand
from myapp.models import Customer


class Command(BaseCommand):
    help = "Update a customer info by id"

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='Customer ID')
        parser.add_argument('name', type=str, help='Customer name')
        parser.add_argument('email', type=str, help='Customer email')
        parser.add_argument('phone_number', type=str, help='Customer phone')
        parser.add_argument('address', type=str, help='Customer address')

    def handle(self, *args, **kwargs):
        pk = kwargs.get('pk')
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone_number = kwargs.get('phone_number')
        address = kwargs.get('address')
        customer = Customer.objects.filter(pk=pk).first()
        customer.name = name
        customer.email = email
        customer.phone_number = phone_number
        customer.address = address
        customer.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated customer: {customer}'))
