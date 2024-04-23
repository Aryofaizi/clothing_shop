from django.shortcuts import render, get_object_or_404, reverse, redirect
from orders.models import Order,OrderItem
from store.models import ProductVariant
import requests
import json
from decouple import config
from django.http import HttpResponse
from django.db import transaction

def payment_process(request):
    order_id =request.session["order_id"]
    order = get_object_or_404(Order, id=order_id)
    price = order.get_order_price()
    
    zarinpal_url ="https://api.zarinpal.com/pg/v4/payment/request.json"
    headers = {
        "accept": "application/json",
        "content_type": "application/json"
    }
    
    data = {
        "merchant_id" : config("merchant_id"),
        "amount" :price,
        "description" : f"#{order.id}  {order.user.first_name} {order.user.last_name}" ,
        "callback_url" : "http://127.0.0.1:8000" + reverse("payment_callback"),
    }
    
    res = requests.post(url=zarinpal_url, data=data, headers=headers)
    res_data = res.json()["data"]
    authority = res_data["authority"]
    order.zarinpal_authority = authority
    order.save()
    
    if "errors" not in res_data or len(res_data["errors"]) == 0:
        return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
    else:
         return HttpResponse("error from zarinpal")


@transaction.atomic
def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get("Status")
    order_id = request.session["order_id"]
    order = get_object_or_404(Order, id = order_id)
    price = order.get_order_price()
    
    if payment_status == "OK": 
        headers = {
        "accept": "application/json",
        "content_type": "application/json"
    }
        
        data = {
        "merchant_id" : config("merchant_id"),
        "amount" :price,
        "authority" : payment_authority,
    }
        res_data = requests.post(
            url="https://api.zarinpal.com/pg/v4/payment/verify.json",
            data = json.dumps(data),
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
                
                return HttpResponse("order payed successfully")
            elif payment_code == 101:
                return HttpResponse("order payed successfully, but this order has already saved in database")
            else:
                return HttpResponse("order unsuccessfull")
        else:
            return HttpResponse("error from zarinpal")
        
    else:
        return HttpResponse("error from zarinpal")
    
    