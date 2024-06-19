from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem, Order

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
                    size = item["size"]
                    color = item["color"]
                    unit_price = int(item["total_price"] / item["quantity"])
                    OrderItem.objects.create(
                        order = form_obj,
                        product = product,
                        size = size,
                        color = color,
                        quantity = item["quantity"],
                        price = unit_price,
                        total = item["total_price"]
                    )
                cart.clear()
                request.user.first_name = form_obj.first_name
                request.user.last_name = form_obj.last_name
                request.user.save()
                
                #send order id as session
                request.session["order_id"] = form_obj.id
                if "single" in request.POST:
                    return redirect("payment_process")
                elif "bulk" in request.POST:
                    invoice = Order.objects.prefetch_related("items").get(id=form_obj.id)
                    return render(request, "store/invoice.html", context={"invoice": invoice})
            
        
    return render(request, "orders/order_create.html",
                  context={"form": form})
