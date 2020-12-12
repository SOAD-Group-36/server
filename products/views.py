from auth.permissions import IsSeller
from auth.authentication import SellerServicesAuthentication
from rest_framework import viewsets
from . import models
from . import serializers
from drf_yasg.utils import swagger_auto_schema


class ProductViewset(viewsets.ModelViewSet):
    authentication_classes = (SellerServicesAuthentication,)
    permission_classes = (IsSeller,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
