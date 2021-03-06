from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from sellers.models import Seller
from utils.address import AddressSerializerField


class SellerSerializer(ModelSerializer):
    firstName = CharField(source='first_name', allow_blank=True, max_length=150, required=False)
    lastName = CharField(source='last_name', allow_blank=True, max_length=150, required=False)
    address = AddressSerializerField()

    class Meta:
        model = Seller
        fields = [
            'id',
            'firstName',
            'lastName',
            'address',
            'email',
            'phone',
            'pan',
            'gst',
        ]
        extra_kwagrs = {'id': {'read_only': True}}
