from django import forms
from .models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'customer_name', 'password', 'phone_number')
