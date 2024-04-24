from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Prefetch
from . import models, forms
from cart.forms import AddToCartProductForm
import json

class HomeView(generic.ListView):
    queryset = models.Product.objects.prefetch_related("images")
    template_name = "store/home.html"
    context_object_name = "products"
    paginate_by = 12
    
    
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
        context["sizes"] = models.Size.objects.filter(size_variants__product=context["product"]).distinct()
        context["colors"] = models.Color.objects.filter(color_variants__product=context["product"]).distinct()
        variants = models.ProductVariant.objects.filter(product = context["product"])
        size_and_color = {}
        for item in variants:
            if item.size.id in size_and_color:
                size_and_color[item.size.id].append({'id': item.color.id, 'title': item.color.title, "quantity":item.quantity})
            else:
                size_and_color[item.size.id] = [{'id': item.color.id, 'title': item.color.title, "quantity":item.quantity}]
            
        context["size_and_color_json"] = json.dumps(size_and_color)
            
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
    