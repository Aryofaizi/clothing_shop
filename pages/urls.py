from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.Contact.as_view(), name="contact_page"),
    path("user_profile/", views.UserProfile.as_view(), name="user_profile_page"),
]
