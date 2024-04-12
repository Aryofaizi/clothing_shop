from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = models.Product


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    
    
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = models.ProductImage