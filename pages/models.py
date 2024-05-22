from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

class Message(models.Model):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), max_length=254)
    subject = models.CharField(_("subject"), max_length=250)
    text = models.TextField(_("message text"))
    datetime_created = models.DateTimeField(_("created"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("modified"), auto_now=True)
    
    def get_absolute_url(self):
        return reverse("contact_page")
    
