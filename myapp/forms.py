from django import forms
from .models import Customer, Order, Product


class CustomerForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    def save(self):
        cleaned_data = self.cleaned_data
        customer = Customer.objects.create(
            name=cleaned_data['name'],
            email=cleaned_data['email'],
            phone_number=cleaned_data['phone_number'],
            address=cleaned_data['address']
        )
        return customer


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    quantity = forms.IntegerField(min_value=1)
    image = forms.ImageField()

    def save(self):
        cleaned_data = self.cleaned_data
        product = Product.objects.create(
            name=cleaned_data['name'],
            description=cleaned_data['description'],
            price=cleaned_data['price'],
            quantity=cleaned_data['quantity'],
            image=cleaned_data['image']
        )
        return product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'products']
