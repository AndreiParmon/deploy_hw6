from django.core.management.base import BaseCommand
from myapp.models import Order, Customer, Product


class Command(BaseCommand):
    help = "Update an order"

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='ID of the order to update')
        parser.add_argument('customer_id', type=int, help='ID of the new customer')
        parser.add_argument('product_ids', type=int, nargs='+', help='IDs of the products to add to the order')

    def handle(self, *args, **kwargs):
        # обнуляем сумму заказа
        total_amount = 0
        order_id = kwargs['order_id']
        customer_id = kwargs['customer_id']
        product_ids = kwargs['product_ids']

        # проверяем есть ли у нас заказ и клиент с заданным id
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order with ID {order_id} does not exist'))
            return
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Customer with ID {customer_id} does not exist'))
            return

        order.customer = customer

        # очищаем существующие продукты и добавляем новые по переданным id
        order.products.clear()
        for product_id in product_ids:
            try:
                product = Product.objects.get(pk=product_id)
                order.products.add(product)
                total_amount += product.price
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Product with ID {product_id} does not exist'))
                return
        order.total_amount = total_amount
        order.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated order: {order}'))
