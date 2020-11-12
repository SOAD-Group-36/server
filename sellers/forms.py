from django import forms

from sellers.models import Seller
from utils.address import AddressFormField


class SellerForm(forms.ModelForm):
    address = AddressFormField()

    class Meta:
        model = Seller
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address', 'pan', 'gst']
