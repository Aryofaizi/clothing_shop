"""Represents cart class."""
from store.models import Product, Size, Color

class Cart():
    def __init__(self, request):
        """Initilize cart."""
        self.request = request
        self.session = self.request.session
        
        cart = self.session.get("cart")
        
        if not cart : 
            cart = self.session["cart"] = {}
            
        self.cart = cart 
            
        
    def add(self, product, size, color, quantity=1, replace_quantity=False):
        """Add specified product to cart if cart exists."""
        product_id = str(product.id)
        index = f"{product_id}, {size}, {color}"
        if index not in self.cart:
            self.cart[index] = {"quantity":0, "color":color, "size": size}
        if replace_quantity:
            self.cart[index]["quantity"] = quantity
        else:
            self.cart[index]["quantity"] += quantity
            
        self.save()
    
    def remove(self, product,size, color):
        """Remove specified product from cart."""
        product_id = str(product.id)
        index = f"{product_id}, {size}, {color}"
        if index in self.cart:
            del self.cart[index]
            self.save()
    
    def save(self):
        """Mark session as modified to save changes"""
        self.session.modified = True
        
        
    
    def __iter__(self):
        """Makes cart iterable."""    
        product_ids = [int(key.split(",")[0]) for key in self.cart.keys()]
        
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        print(cart)
        for key in self.cart.keys():
            splited_key = key.split(",")
            size = splited_key[1]
            color = splited_key[2]
            for product in products:
                cart[f"{product.id},{size},{color}"]["product_obj"] = product
                cart[f"{product.id},{size},{color}"]["color"] = Color.objects.get(id=color)
                cart[f"{product.id},{size},{color}"]["size"] = Size.objects.get(id=size)
                
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
            
            
            
        
            