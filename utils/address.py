import json

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.safestring import mark_safe
from drf_yasg import openapi
from rest_framework import serializers


class Address:
    def __init__(
        self,
        pincode: str,
        state: str,
        city: str,
        landmark: str = '',
        house_no: str = '',
        street_name: str = '',
        **kwargs,
    ):
        self.house_no = house_no or kwargs.get("houseNo", '')
        self.street_name = street_name or kwargs.get("street_name", '')
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

    def __str__(self):
        return f'{self.house_no} {self.street_name} {self.city} {self.state} {self.pincode}'

    def as_list(self):
        return [self.pincode, self.state, self.city, self.landmark, self.house_no, self.street_name]

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
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Address",
            "properties": {
                "pincode": openapi.Schema(
                    title="Pin Code",
                    type=openapi.TYPE_STRING,
                ),
                "state": openapi.Schema(
                    title="State",
                    type=openapi.TYPE_STRING,
                ),
                "city": openapi.Schema(
                    title="City",
                    type=openapi.TYPE_STRING,
                ),
                "landmark": openapi.Schema(
                    title="Landmark",
                    type=openapi.TYPE_STRING,
                ),
                "houseNo": openapi.Schema(
                    title="House No",
                    type=openapi.TYPE_STRING,
                ),
                "streetName": openapi.Schema(
                    title="Street Name",
                    type=openapi.TYPE_STRING,
                ),
            },
            "required": ["pincode", "state", "city"],
        }

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


class AddressWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = {
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'landmark': forms.TextInput(attrs={'placeholder': 'Landmark'}),
            'house_no': forms.TextInput(attrs={'placeholder': 'House_no'}),
            'street': forms.TextInput(attrs={'placeholder': 'Street'}),
        }
        super(AddressWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value and type(value) == Address:
            return value.as_list()
        else:
            return ['', '', '', '', '', '']


class AddressFormField(forms.MultiValueField):
    widget = AddressWidget
    default_error_messages = {
        'invalid': 'Enter a list of values.',
        'incomplete': 'Enter a complete value.',
    }

    def __init__(self, **kwargs):
        fields = [
            forms.RegexField(label='Pin Code', regex=r'[0-9]{6}', strip=True),
            forms.CharField(label='State', max_length=100),
            forms.CharField(label='City', max_length=100),
            forms.CharField(label='Landmark', max_length=160, required=False),
            forms.CharField(label='House No', max_length=160, required=False),
            forms.CharField(label='Street', max_length=160, required=False),
        ]
        super().__init__(fields, required=False, **kwargs)
        self.fields = fields

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.fields = tuple(x.__deepcopy__(memo) for x in self.fields)
        return result

    def prepare_value(self, value):
        return value

    def validate(self, value):
        pass

    def compress(self, data_list):
        if type(data_list) is list:
            return Address(*data_list)
        if type(data_list) is dict:
            return Address(**data_list)
        raise NotImplemented

    def has_changed(self, initial, data):
        if self.disabled:
            return False
        if initial is None:
            initial = ['' for x in range(0, len(data))]
        else:
            if not isinstance(initial, list):
                initial = self.widget.decompress(initial)
        for field, initial, data in zip(self.fields, initial, data):
            try:
                initial = field.to_python(initial)
            except ValidationError:
                return True
            if field.has_changed(initial, data):
                return True
        return False
