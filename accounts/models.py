from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """A class to customize user model."""
    pass