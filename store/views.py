from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from . import models

class HomeView(generic.ListView):
    queryset = models.Product.objects.prefetch_related("images")
    template_name = "store/home.html"
    context_object_name = "products"
    
    
class ProductDetailView(generic.DetailView):
    model = models.Product
    template_name = "store/product_detail.html"
    context_object_name = "product"
    