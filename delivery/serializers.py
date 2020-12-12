from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import LogisticServices, Delivery
from utils.address import AddressSerializerField
from orders.serializers import OrderSerializer


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


class DeliverySerializer(ModelSerializer):
    order = OrderSerializer(read_only=True)
    service = LogisticSerializer(read_only=True)
    origin = AddressSerializerField()
    current = AddressSerializerField()
    destination = AddressSerializerField()
    receiver = SlugRelatedField("full_name", read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'order',
            'service',
            'current',
            'origin',
            'destination',
            'receiver',
            'status',
        ]
