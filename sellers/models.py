from django.db import models


class Seller(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(unique=True, max_length=13)
    pan = models.CharField(unique=True, max_length=13)
    gst = models.CharField(unique=True, max_length=13)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
