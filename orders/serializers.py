from rest_framework.serializers import ModelSerializer, SlugRelatedField
from orders.models import Order
from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
        ]


class OrderSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = SlugRelatedField("get_full_name", read_only=True)

    class Meta:
        model = Order
        fields = ["user", "product", "quantity", "price", "placed_on", "status"]
