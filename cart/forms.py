from django import forms


class AddToCartProductForm(forms.Form):
    choices = [(i, str(i)) for i in range(1,31)]
    
    quantity = forms.TypedChoiceField(choices=choices, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)