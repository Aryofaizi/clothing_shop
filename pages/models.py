from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Message(models.Model):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), max_length=254)
    subject = models.CharField(_("subject"), max_length=250)
    text = models.TextField(_("message text"))
    datetime_created = models.DateTimeField(_("created"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("modified"), auto_now=True)
    
    def get_absolute_url(self):
        return reverse("contact_page")
    
    
    
class Blog(models.Model):
    title = models.CharField(_("title"), max_length=255)
    text = models.TextField(_("text"))
    quote = models.TextField(_("quote"), null=True, blank=True)
    quote_author = models.CharField(_("quote author"), max_length=255, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), verbose_name=_("author"), on_delete=models.CASCADE)
    author_bio = models.TextField(_("author bio"))
    datetime_created = models.DateTimeField(_("created"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("modified"), auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk":self.id})
    
    
    
    
    
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=_("blog"), on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("image"), upload_to="blog_images", blank=True)
    

    def __str__(self):
        return f"{self.blog} + image"
    
    
    
