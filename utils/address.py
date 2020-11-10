import json

from django.db import models
from rest_framework import serializers


class Address:
    def __init__(
        self,
        pincode: str,
        state: str,
        city: str,
        landmark: str = None,
        house_no: str = None,
        street_name: str = None,
        **kwargs,
    ):
        self.house_no = house_no or kwargs.pop("houseNo")
        self.street_name = street_name or kwargs.pop("street_name")
        self.landmark = landmark
        self.pincode = pincode
        self.state = state
        self.city = city

    def __dict__(self) -> dict:
        return {
            "house_no": self.house_no,
            "street_name": self.street_name,
            "landmark": self.landmark,
            "pincode": self.pincode,
            "state": self.state,
            "city": self.city,
        }

    def json(self):
        return json.dumps(self.__dict__())


class AddressField(models.Field):
    default_error_messages = {"invalid": "'%s' is not a valid Address."}
    description = "Address object"

    def __init__(self, *args, **kwargs):
        if not kwargs.get("null", False):
            kwargs["default"] = kwargs.get("default", dict())
        super(AddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def db_type(self, connection):
        if connection.vendor == "postgresql":
            # Only do jsonb if in pg 9.4+
            if connection.pg_version >= 90400:
                return "jsonb"
            return "text"
        if connection.vendor == "mysql":
            return "longtext"
        if connection.vendor == "oracle":
            return "long"
        return "text"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        elif connection.vendor == "postgresql":
            data = value
        data = json.loads(value)
        return Address(**data)

    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)

    def get_prep_value(self, value: Address):
        if value is None:
            if not self.null and self.blank:
                return ""
            return None
        return value.json()

    def select_format(self, compiler, sql, params):
        if compiler.connection.vendor == "postgresql":
            return "%s::text" % sql, params
        return super(AddressField, self).select_format(compiler, sql, params)

    def value_to_string(self, obj):
        return self.value_from_object(obj)


class AddressSerializerField(serializers.Field):
    def to_internal_value(self, data):
        """
        Do not serialize it to JSON yet.
        We need the field data to be a python object in serializer.validated_data
        :param data:
        :return:
        """
        assert type(data) == dict
        assert "pincode" in data
        assert "state" in data
        assert "city" in data
        return Address(**data)

    def to_representation(self, value):
        """
        Load field json to a python object from existing object
        :param value:
        :return: native python object
        """
        assert type(value) == Address
        value = value.__dict__()
        return value
