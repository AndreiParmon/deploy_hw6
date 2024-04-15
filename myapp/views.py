from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .forms import CustomerForm, OrderForm, ProductForm
from .models import Customer, Order, Product


def index(request):
    context = {
        'title': 'Добро пожаловать!',
    }
    return render(request, 'myapp/index.html', context)


# ---------------------------------------------------------------------------------------------------
def fetch_customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'myapp/customer_list.html', {'customers': customers})


def fetch_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'myapp/customer_detail.html', {'customer': customer})


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            customer = Customer(
                name=name,
                email=email,
                phone_number=phone_number,
                address=address
            )
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
        message = 'Заполните форму!'
    return render(request, 'myapp/add_customer.html', {'form': form, 'message': message})


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer.name = form.cleaned_data['name']
            customer.email = form.cleaned_data['email']
            customer.phone_number = form.cleaned_data['phone_number']
            customer.address = form.cleaned_data['address']
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(initial={
            'name': customer.name,
            'email': customer.email,
            'phone_number': customer.phone_number,
            'address': customer.address
        })
    return render(request, 'myapp/edit_customer.html', {'form': form, 'customer': customer})


# ---------------------------------------------------------------------------------------------------

def fetch_order_list(request):
    orders = Order.objects.all()
    return render(request, 'myapp/order_list.html', {'orders': orders})


def fetch_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'myapp/order_detail.html', {'order': order})


def fetch_customer_orders(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Order.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'myapp/orders.html', context)


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            form.save_m2m()
            return redirect('add_customer_products', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'myapp/create_order.html', {'form': form})


def add_customer_products(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save_m2m()
            form.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'myapp/add_customer_products.html', {'form': form, 'order': order})


# ---------------------------------------------------------------------------------------------------

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            image = form.cleaned_data['image']
            product = Product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                image=image
            )
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
        message = 'Заполните форму!'
    return render(request, 'myapp/add_product.html', {'form': form, 'message': message})


def fetch_product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/product_list.html', {'products': products})


def fetch_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'myapp/product_detail.html', {'product': product})


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.quantity = form.cleaned_data['quantity']
            product.image = form.cleaned_data['image']
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'quantity': product.quantity,
            'image': product.image
        })
    return render(request, 'myapp/edit_product.html', {'form': form, 'product': product})
