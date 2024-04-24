from django.contrib import admin
from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    fields = ("author", "text", "rate", "status")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    inlines = (
        CommentInline,
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    
    
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = models.ProductImage
    

@admin.register(models.Comment)
class Comment(admin.ModelAdmin):
    model = models.Comment
    list_display = ("status","checked","rate","text","datetime_created","author")
@admin.register(models.ProductVariant)
class ProductVariant(admin.ModelAdmin):
    model = models.ProductVariant
    
@admin.register(models.Color)
class Color(admin.ModelAdmin):
    model = models.Color
    
    
@admin.register(models.Size)
class Size(admin.ModelAdmin):
    model = models.Size