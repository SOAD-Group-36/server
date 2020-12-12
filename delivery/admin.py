from django.contrib import admin
from .models import LogisticServices
from utils.address import AddressFormField

# Register your models here.
@admin.register(LogisticServices)
class LogisticSeriveAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"] = AddressFormField()
        return form