from users.models import ApiKey
from django.contrib import admin

from sellers.models import Seller
from utils.address import AddressFormField


class APIKeyInline(admin.TabularInline):
    model = ApiKey
    extra = 0


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"] = AddressFormField()
        return form

    inlines = [
        APIKeyInline,
    ]
