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
        for key, item in self.cart.items():
            product_id, size, color_id = key.split(",")
            try:
                product = Product.objects.get(id=int(product_id))
                color = Color.objects.get(id=int(color_id))
                size = Size.objects.get(id=int(size))
                item["product_obj"] = product
                item["color"] = color
                item["size"] = size
                item["total_price"] = item["quantity"] * product.price
                yield item
            except (Product.DoesNotExist, Color.DoesNotExist, Size.DoesNotExist, ValueError) as e:
                print(f"Error processing item {key}: {e}")

            
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
            
    def get_total_price_with_tax(self):
        """Returns cart total price with tax."""
        total = self.get_total_price()
        return total + 50_000
            
        
            