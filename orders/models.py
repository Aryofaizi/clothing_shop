from django.db import models
from store.models import Product
from django.contrib.auth import get_user_model

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    note = models.CharField(max_length=700)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderitems")
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return f"order : {self.order} : {self.product}"
    
    
    
    
    
    
    
