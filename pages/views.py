from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from . import models, forms
from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
class Contact(generic.CreateView):
    form_class = forms.MessageForm
    template_name = "pages/contact.html"
    


class UserProfile(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = "pages/user_profile.html"
    form_class = CustomUserChangeForm
    
    def get_object(self, queryset=None):
        return self.request.user
    
    
    
def vendor_store(request):
    return render(request, "pages/vendor_store.html")



class BlogListView(generic.ListView):
    model = models.Blog
    template_name = "pages/blog.html"
    context_object_name = "blogs"
    
    
    
class BlogDetailView(generic.DetailView):
    model = models.Blog
    template_name = "pages/blog_detail.html"