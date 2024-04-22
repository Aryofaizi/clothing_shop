from django import forms
from store.models import ProductVariant
from django.shortcuts import get_object_or_404

class AddToCartProductForm(forms.Form):
    choices = [(i, str(i)) for i in range(1,31)]
    quantity = forms.TypedChoiceField(choices=choices, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)    
    color = forms.TypedChoiceField(choices=choices, coerce=int)
    size = forms.TypedChoiceField(choices=choices, coerce=int)
    
    
    
class RemoveFromCartProductForm(forms.Form):
    choices = [(i, str(i)) for i in range(1,31)]
    color = forms.TypedChoiceField(choices=choices, coerce=int)
    size = forms.TypedChoiceField(choices=choices, coerce=int)
        
        