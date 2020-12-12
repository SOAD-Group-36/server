from django.contrib import admin

from sellers.models import Seller,SellerDelivery
from utils.address import AddressFormField

admin.site.register(SellerDelivery)
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"] = AddressFormField()
        return form
