from django import forms
from django.contrib.auth.forms import UserCreationForm

from delivery.models import LogisticServices
from utils.address import AddressFormField


class LogisticServiceForm(forms.ModelForm):
    address = AddressFormField()

    class Meta:
        model = LogisticServices
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address', 'pan', 'gst']


class SellerRegistrationForm(UserCreationForm):
    address = AddressFormField()

    def address_fields(self):
        for i in self:
            if i.widget_type == 'address':
                return i.subwidgets[0].data['subwidgets']

    class Meta:
        model = LogisticServices
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
