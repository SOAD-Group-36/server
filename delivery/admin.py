from users.models import ApiKey
from django.contrib import admin
from .models import LogisticServices
from utils.address import AddressFormField


class APIKeyInline(admin.TabularInline):
    model = ApiKey
    extra = 0


@admin.register(LogisticServices)
class LogisticSeriveAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"] = AddressFormField()
        return form

    inlines = [
        APIKeyInline,
    ]
