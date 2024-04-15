"""Represents cart class."""
from store.models import Product

class Cart():
    def __init__(self, request):
        """Initilize cart."""
        self.request = request
        self.session = self.request.session
        
        cart = self.session.get("cart")
        
        if not cart : 
            cart = self.session["cart"] = {}
            
        self.cart = cart 
            
        
    def add(self, product, quantity=1, replace_quantity=False):
        """Add specified product to cart if cart exists."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity":0}
        if replace_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
            
        self.save()
    
    def remove(self, product):
        """Remove specified product from cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """Mark session as modified to save changes"""
        self.session.modified = True
        
        
    
    def __iter__(self):
        """Makes cart iterable."""
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]["product_obj"] = product
            
        for item in cart.values():
            item["total_price"] = item["quantity"] * item["product_obj"].price
            yield item
            
    def __len__(self):
        """Returns cart items length."""
        return sum(item["quantity"] for item in self.cart.values())
    

    def clear(self):
        """Removes all cart items."""
        del self.session["cart"]
        self.save()
        
        
    def get_total_price(self):
        """Returns cart total price."""
        return sum(item["quantity"]*item["product_obj"].price for item in self.cart.values())
            
            
            
        
            