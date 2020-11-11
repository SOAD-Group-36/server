from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from .models import LogisticServices
from utils.address import AddressSerializerField


class LogisticSerializer(ModelSerializer):
    firstName = CharField(source='first_name', allow_blank=True, max_length=150, required=False)
    lastName = CharField(source='last_name', allow_blank=True, max_length=150, required=False)
    address = AddressSerializerField()

    class Meta:
        model = LogisticServices
        fields = [
            'firstName',
            'lastName',
            'address',
            'phone',
            'pan',
            'gst',
        ]
