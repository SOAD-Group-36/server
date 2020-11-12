from rest_framework import mixins
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from sellers.models import Seller
from sellers.serializers import SellerSerializer


class SellerViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
