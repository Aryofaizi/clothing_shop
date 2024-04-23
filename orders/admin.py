from django.contrib import admin

from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ("order", "product", "quantity", "size", "color", "price")


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ("user", "is_paid", "first_name", "last_name","phone_number","address","note","post_id","has_been_sent")
    inlines = (
        OrderItemInline,
    )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = models.OrderItem
