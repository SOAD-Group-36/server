from uuid import uuid4

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(unique=True, max_length=12)


class Business(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)


class ApiKey(models.Model):
    key = models.UUIDField(default=uuid4)
    business = models.ForeignKey("users.Business", on_delete=models.CASCADE, related_name="api_keys")
