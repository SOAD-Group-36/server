from django import forms
from django.contrib.auth.forms import UserCreationForm

from sellers.models import Seller
from utils.address import AddressFormField


class SellerForm(forms.ModelForm):
    address = AddressFormField()

    class Meta:
        model = Seller
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address', 'pan', 'gst']


class SellerRegistrationForm(UserCreationForm):
    address = AddressFormField()

    def address_fields(self):
        for i in self:
            if i.widget_type == 'address':
                return i.subwidgets[0].data['subwidgets']

    class Meta:
        model = Seller
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'pan',
            'gst',
            'password1',
            'password2',
        ]
