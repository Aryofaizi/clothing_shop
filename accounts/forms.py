from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """A custom form to create for user model."""
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        

class CustomUserChangeForm(UserChangeForm):
    """A custom form to change data in user model."""
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("This email address is already in use."))
        return email