from django.contrib import admin

from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ("order", "product", "quantity", "price")


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    inlines = (
        OrderItemInline,
    )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = models.OrderItem
