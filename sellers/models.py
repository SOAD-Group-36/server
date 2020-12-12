from django.db import models

from users.models import Business
from utils.address import AddressField


class Seller(Business):
    is_seller = True

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(unique=True, max_length=13)
    address = AddressField()
    pan = models.CharField(unique=True, max_length=13)
    gst = models.CharField(unique=True, max_length=13)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    webhook_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + self.last_name

