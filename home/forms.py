from django.template.defaultfilters import default
from utils.address import AddressFormField
from django import forms
from sellers.models import Seller
from orders.models import Order


class OrderPlaceForm(forms.Form):
    address = AddressFormField()
    quantity = forms.IntegerField(required=True, min_value=1)

    def address_fields(self):
        for i in self:
            if i.widget_type == 'address':
                return i.subwidgets[0].data['subwidgets']
