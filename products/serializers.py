from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from products.models import Product


class ProductSerializer(ModelSerializer):
    images = SlugRelatedField(many=True, read_only=True, slug_field="url")

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "name",
            "description",
            "stock",
            "price",
            "weight",
            "length",
            "height",
            "width",
            "images",
        ]
