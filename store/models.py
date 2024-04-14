from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """Represent category obj in database."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    inventory = models.PositiveSmallIntegerField(default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return category title."""
        return self.title

class Product(models.Model):
    PRODUCT_RATE_FIVE_STAR = 5
    PRODUCT_RATE_FOUR_STAR = 4
    PRODUCT_RATE_THREE_STAR = 3
    PRODUCT_RATE_TWO_STAR = 2
    PRODUCT_RATE_ONE_STAR = 1
    PRODUCT_RATE_CHOICES = [
        (PRODUCT_RATE_FIVE_STAR, "EXCELLENT"),
        (PRODUCT_RATE_FOUR_STAR, "GOOD"),
        (PRODUCT_RATE_THREE_STAR, "NOT BAD"),
        (PRODUCT_RATE_TWO_STAR, "BAD"),
        (PRODUCT_RATE_ONE_STAR, "VERY BAD"),
    ]
    """Represent product obj in database."""
    title = models.CharField(max_length=255)
    rate = models.IntegerField(choices=PRODUCT_RATE_CHOICES)
    price = models.PositiveIntegerField()
    description = models.TextField()
    code = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    seller_name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        """Return product title."""
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    
    
    
    
    
class Size(models.Model):
    """Represent a size obj in database."""
    title = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return product title."""
        return self.title
    
class Color(models.Model):
    """Represent a color obj in database."""
    title = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return product title."""
        return self.title
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.title} - {self.size.title} - {self.color.title}"


class ProductImage(models.Model):
    """Represent image obj for product in database."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images", blank=True)
    
    def __str__(self):
        return self.product.title + "Image"
    


class Comment(models.Model):
    COMMENT_RATE_FIVE_STAR = 5
    COMMENT_RATE_FOUR_STAR = 4
    COMMENT_RATE_THREE_STAR = 3
    COMMENT_RATE_TWO_STAR = 2
    COMMENT_RATE_ONE_STAR = 1
    COMMENT_RATE_CHOICES = [
        (COMMENT_RATE_FIVE_STAR, "EXCELLENT"),
        (COMMENT_RATE_FOUR_STAR, "GOOD"),
        (COMMENT_RATE_THREE_STAR, "NOT BAD"),
        (COMMENT_RATE_TWO_STAR, "BAD"),
        (COMMENT_RATE_ONE_STAR, "VERY BAD"),
    ]
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name= _("comment text"))
    rate = models.IntegerField(verbose_name= _("rate"), choices=COMMENT_RATE_CHOICES)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.author} : {self.text[:20]} ..."
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.product.id})
    