from django.db import models
from store.models import Product
from django.contrib.auth import get_user_model
from store.models import Size, Color

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    note = models.CharField(max_length=700, blank=True)
    post_id = models.CharField(max_length=12)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=150, blank=True)
    zarinapl_data = models.TextField(blank=True)
    has_been_sent  = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id}"
    
    def get_order_price(self):
        return sum(item.quantity * item.price for item in self.items.all())
    
    def get_order_price_with_tax(self):
        return self.get_order_price + 50_000
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderitems")
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"order : {self.order} : {self.product}"
    
    
    
    
    
    
    
