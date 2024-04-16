from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
import requests
import json
from django.http import HttpResponse


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
        "merchant_id" : "",
        "amount" :price,
        "description" : f"#{order.id}  {order.user.first_name} {order.user.last_name}" ,
        "callback_url" : "http://127.0.0.1:8000",
    }
    
    res = requests.post(url=zarinpal_url, data=json.dumps(data), headers=headers)
    
    res_data = res.json()["data"]
    authority = res_data["authority"]
    order.zarinpal_authority = authority
    order.save()
    
    if "errors" not in res_data or len(res_data["errors"]) == 0:
        return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
    else:
         return HttpResponse("error from zarinpal")
