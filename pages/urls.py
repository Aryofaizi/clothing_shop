from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.Contact.as_view(), name="contact_page"),
    path("user_profile/", views.UserProfile.as_view(), name="user_profile_page"),
    path("vendor_store/", views.vendor_store, name="vendor_store_page"),
    path("blog_page/", views.BlogListView.as_view(), name="blog_page"),
]
