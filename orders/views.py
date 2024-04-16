from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem

@login_required
def order_create_view(request):
    form = OrderForm()
    cart = Cart(request)
    
    if len(cart) == 0:
        return redirect("home_page")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.save()
            
            for item in cart:
                product = item["product_obj"]
                OrderItem.objects.create(
                    order = form_obj,
                    product = product,
                    quantity = item["quantity"],
                    price = item["product_obj"].price,
                )
            cart.clear()
            request.user.first_name = form_obj.first_name
            request.user.last_name = form_obj.last_name
            request.user.save()
            
            #send order id as session
            request.session["order_id"] = form_obj.id
            return redirect("payment_process")
        
    return render(request, "orders/order_create.html",
                  context={"form": form})
