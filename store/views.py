from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Prefetch
from . import models, forms
from cart.forms import AddToCartProductForm

class HomeView(generic.ListView):
    queryset = models.Product.objects.prefetch_related("images")
    template_name = "store/home.html"
    context_object_name = "products"
    
    
class ProductDetailView(generic.DetailView):
    queryset = models.Product.objects.prefetch_related(
        Prefetch("comments", queryset= models.Comment.objects.select_related("author").filter(status="a"))
    )
    template_name = "store/product_detail.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = forms.CommentForm()
        context["add_to_cart_form"] = AddToCartProductForm()
        return context
    
    
    
class CommentCreateView(generic.CreateView):
    model = models.Comment
    form_class = forms.CommentForm
    
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        product_id = int(self.kwargs["pk"])
        product = get_object_or_404(models.Product, id = product_id)
        obj.product = product
        return super().form_valid(form)
    