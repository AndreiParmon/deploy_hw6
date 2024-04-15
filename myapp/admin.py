import csv
from django.contrib import admin
from django.http import HttpResponse
from django.db import models
from django.utils.safestring import mark_safe
from .models import Customer, Order, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Для списка клиентов"""
    list_display = ['name', 'email', 'phone_number', 'address']
    list_filter = ['registration_date']
    readonly_fields = ['registration_date']
    search_fields = ['name', 'phone_number']
    search_help_text = 'Поиск клиента по имени и номеру телефона'
    """Для отдельного клиента"""
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name']
            }
        ),
        (
            'Контакты',
            {
                'description': 'Контактная информация клиента',
                'fields': ['phone_number', 'email'],
            },
        ),
        (
            'Адрес',
            {
                'classes': ['collapse'],
                'description': 'Адрес для доставки',
                'fields': ['address'],
            }
        ),
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['display_id', 'customer', 'total_amount', 'order_date']
    list_filter = ['customer', 'order_date', 'products']
    search_fields = ['customer__name']
    search_help_text = 'Поиск заказа по клиенту'
    readonly_fields = ['order_date']
    actions = ['export_to_csv']
    fieldsets = [
        ('Основная информация', {
            'fields': ['customer', 'total_amount', 'order_date']
        }),
        ('Товары', {
            'fields': ('products',)
        })
    ]
    filter_horizontal = ('products',)

    def save_model(self, request, obj, form, change):
        if not obj.total_amount:
            obj.total_amount = obj.products.aggregate(total=models.Sum('price'))['total']
        super().save_model(request, obj, form, change)
        obj.products.set(form.cleaned_data['products'])
        obj.save()

    def display_id(self, obj):
        return f"Заказ №{obj.id}"

    display_id.short_description = 'Номер заказа'

    @admin.action(description='Экспорт в CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Клиент', 'Сумма заказа', 'Дата заказа'])

        for order in queryset:
            writer.writerow([order.id, order.customer.name, order.total_amount, order.order_date])
        return response


@admin.action(description="Обнулить товарный остаток")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Для списка товаров"""
    list_display = ['name', 'price', 'quantity']
    list_filter = ['added_date', 'price']
    readonly_fields = ['added_date', 'preview']
    search_fields = ['description']
    search_help_text = 'Поиск товара по описанию'
    actions = [reset_quantity]
    """Для отдельного товара"""
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name']
            }
        ),
        (
            'Отдел закупок',
            {
                'fields': ['quantity', 'price'],
                'description': 'Для управления товарными запасами'
            },
        ),
        (
            'Описание товара',
            {
                'classes': ['collapse'],
                'description': 'Подробная информация о товаре',
                'fields': ['description'],
            }
        ),
        (
            'Загрузка изображения',
            {
                'description': 'Добавьте изображение товара',
                'fields': ['image'],
            }
        ),
        (
            'Изображение товара',
            {
                'fields': ['preview'],
            }
        ),
        (
            'Прочее',
            {
                'description': 'Дата добавления',
                'fields': ['added_date'],
            }
        ),
    ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="width: 200px; height: auto;" alt="Изображения нет">')
