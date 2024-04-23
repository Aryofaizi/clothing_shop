from django.shortcuts import render, get_object_or_404, reverse, redirect
from orders.models import Order,OrderItem
from store.models import ProductVariant
from django.utils.translation import gettext as _
import requests
import json
from decouple import config
from django.http import HttpResponse
from django.db import transaction

def payment_process(request):
    order_id =request.session["order_id"]
    order = get_object_or_404(Order, id=order_id)
    price = order.get_order_price_with_tax()
    price_in_rial = price * 10
    
    zarinpal_url ="https://api.zarinpal.com/pg/v4/payment/request.json"
    headers = {
        "accept": "application/json",
        "content_type": "application/json"
    }
    
    data = {
        "merchant_id" : config("merchant_id"),
        "amount" :price_in_rial,
        "description" : f"#{order.id}  {order.user.first_name} {order.user.last_name}" ,
        "callback_url" : "http://tounique.ir" + reverse("payment_callback"),
    }
    
    res = requests.post(url=zarinpal_url, data=data, headers=headers)
    res_data = res.json()["data"]
    authority = res_data["authority"]
    order.zarinpal_authority = authority
    order.save()
    
    if "errors" not in res_data or len(res_data["errors"]) == 0:
        return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
    else:
        return render(request, "back_to_site.html", context={
            "header":_("error from zarinpal"),
            "body": _("error from zarinpal order is not saved if the payment took money from your account it will withdraw automatically after72 hours")
            })


@transaction.atomic
def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get("Status")
    order_id = request.session["order_id"]
    order = get_object_or_404(Order, id = order_id)
    price = order.get_order_price_with_tax() * 10
    price_in_rial = price * 10
    
    if payment_status == "OK": 
        headers = {
        "accept": "application/json",
        "content_type": "application/json"
    }
        
        data = {
        "merchant_id" : config("merchant_id"),
        "amount" :price_in_rial,
        "authority" : payment_authority,
    }
        res_data = requests.post(
            url="https://api.zarinpal.com/pg/v4/payment/verify.json",
            data = data,
            headers=headers,
            )
        if "errors" not in res_data or len(res_data["errors"]) == 0:
            data = res_data.json()["data"]
            payment_code = data["code"]
            if payment_code == 100: 
                order.is_paid = True
                order.zarinpal_ref_id = data["ref_id"]
                order.zarinapl_data = data
                order.save()
                
                #update product variant quantities
                order_items = OrderItem.objects.filter(order=order)
                for order_item in order_items:
                    product = order_item.product
                    size = order_item.size
                    color = order_item.color
                    variant = ProductVariant.objects.get(product=product,size=size,color=color)
                    variant.quantity -= order_item.quantity
                    variant.save()
                
                return render(request, "back_to_site.html", context={
            "header":_("order payed successfully"),
            "body": _("order payed succesffully thanks for you attention your order will be sent soon")
            })
            elif payment_code == 101:
                return render(request, "back_to_site.html", context={
            "header":_("order is repeated"),
            "body": _("order payed successfully but this order was repeated its saved in the database long time ago")
            })
            else:
                return render(request, "back_to_site.html", context={
            "header":_("unsuccessfull order"),
            "body": _("there was a problem in your order order is not successfull")
            })
        else:
            return render(request, "back_to_site.html", context={
            "header":_("unsuccessfull order"),
            "body": _("error from zarinpal try again later")
            })
        
    else:
        return render(request, "back_to_site.html", context={
            "header":_("unsuccessfull order"),
            "body": _("error from zarinpal try again later")
            })
    
    