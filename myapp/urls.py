from django.urls import path
from .views import index
from .views import add_product, fetch_product, fetch_product_list, edit_product
from .views import fetch_customer_orders
from .views import fetch_order_list, fetch_order, create_order, add_customer_products
from .views import add_customer, fetch_customer, fetch_customer_list, edit_customer

urlpatterns = [
    path('', index, name='index'),

    path('add_p/', add_product, name='add_product'),
    path('edit_p/<int:product_id>/', edit_product, name='edit_product'),
    path('product_list/', fetch_product_list, name='product_list'),
    path('product/<int:product_id>/', fetch_product, name='product_view'),

    path('customer-orders/<int:customer_id>', fetch_customer_orders, name='customer_orders'),
    path('order_list/', fetch_order_list, name='order_list'),
    path('order/<int:order_id>/', fetch_order, name='order_view'),
    path('create_order/', create_order, name='create_order'),
    path('order/<int:order_id>/add/', add_customer_products, name='add_customer_products'),

    path('customer_list/', fetch_customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', fetch_customer, name='customer_view'),
    path('edit_c/<int:customer_id>/', edit_customer, name='edit_customer'),
    path('add_c/', add_customer, name='add_customer'),
]
