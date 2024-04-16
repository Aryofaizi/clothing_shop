from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from .forms import AddToCartProductForm
from store.models import Product
from django.views.decorators.http import require_POST

def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item["product_update_quantity_form"] = AddToCartProductForm(initial={
            "quantity" : item["quantity"],
            "inplace" : True,
        })
    return render(request, "cart/cart_detail.html",context={"cart":cart})


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    form = AddToCartProductForm(request.POST)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data["quantity"]
        inplace = cleaned_data["inplace"]
        cart.add(product,quantity,inplace)
    
    return redirect("cart_detail")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    return redirect("cart_detail")

@require_POST
def clear_cart(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
    return redirect("cart_detail")