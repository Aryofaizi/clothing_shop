from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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
        fields = UserChangeForm.Meta.fields