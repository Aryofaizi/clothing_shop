from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class CustomUser(AbstractUser):
    """A class to customize user model."""
    pass

    def get_absolute_url(self):
        return reverse("user_profile_page")
    