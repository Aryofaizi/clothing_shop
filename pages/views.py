from django.shortcuts import render
from django.views import generic
from . import models, forms

class Contact(generic.CreateView):
    form_class = forms.MessageForm
    template_name = "pages/contact.html"
    
