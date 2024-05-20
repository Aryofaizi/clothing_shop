from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.db.models import Prefetch
from . import models, forms
from cart.forms import AddToCartProductForm
from django.utils.translation import gettext_lazy as _
import json
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order


class HomeView(generic.ListView):
    queryset = models.Product.objects.prefetch_related("images")
    template_name = "store/home.html"
    context_object_name = "products"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = models.Product.objects.filter(title__icontains=search).prefetch_related("images")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["underwear_products"] = models.Product.objects.filter(category__title__icontains=_("underwear")).prefetch_related("images")
        last_four_products = models.Product.objects.order_by("-id").select_related("category").prefetch_related("images")[:4]
        context['last_four_products'] = last_four_products
        return context
            
    
    
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
    
    
    
    
class CategroyList(generic.DetailView):
    queryset = models.Category.objects.prefetch_related("products")
    template_name = "store/category_list.html"
    
    
    
class CategorySearchList(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        if search:
            try:
                category = models.Category.objects.get(title__icontains=search)
                return redirect(reverse('category_list', kwargs={'pk': category.pk}))
            except Exception:
                # Optionally handle the case where no category is found
                # Replace with appropriate fallback
                previous_page = request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(previous_page)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
       
class UserDashboard(LoginRequiredMixin, generic.ListView):
    template_name = "store/user_dashboard.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        self.queryset = Order.objects.filter(user = self.request.user)
        return self.queryset
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["not_paid_orders"] = self.queryset.filter(is_paid=False)
        context["paid_orders"] = self.queryset.filter(is_paid=True)
        context["sliced_orders"] = Order.objects.filter(user = self.request.user).prefetch_related("items")[:6]
        return context
