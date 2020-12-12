from uuid import uuid4

from django.db import models

from users.models import Business
from utils import AddressField


class LogisticServices(Business):
    is_logistic_service = True

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


class Delivery(models.Model):
    class Status(models.TextChoices):
        PROCESSED = "Pr", "Processed"
        PICKEDUP = "Pu", "Picked Up"
        INTRANSIT = "Tr", "In Transit"
        DELIVERED = "Dl", "Delivered"
        RTTRANSIT = "Rt", "Return Transit"
        RETURNED = "Rc", "Returned To Seller"  # Received Back
        OUTFORDELIVERY = "Do", "Out For Delivery"

    tracking_id = models.UUIDField(default=uuid4, unique=True)  # Public Tracking ID
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery')
    service = models.ForeignKey('delivery.LogisticServices', on_delete=models.CASCADE)
    origin = AddressField()
    current = AddressField()
    destination = AddressField()
    receiver = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PROCESSED)
