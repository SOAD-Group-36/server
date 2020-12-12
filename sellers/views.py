from auth.permissions import IsAuthenticated
from auth.authentication import SellerServicesAuthentication
import requests
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from sellers.forms import SellerRegistrationForm
from orders.models import Order
from orders.serializers import OrderSerializer
from sellers.models import Seller
from delivery.models import LogisticServices,Delivery
from sellers.serializers import SellerSerializer,SellerDeliverySerializer
from delivery.serializers import LogisticSerializer,DeliverySerializer


class SellerViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    authentication_classes = (SellerServicesAuthentication, )
    permission_classes = (IsAuthenticated, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

@swagger_auto_schema(responses = {200:LogisticSerializer(many=True)},method='GET')
@api_view(['GET'])
def deliverylist(request):
    logisticlist = LogisticServices.objects.all()
    serializer = LogisticSerializer(logisticlist,many=True)
    return Response(serializer.data)

@swagger_auto_schema(request_body = SellerDeliverySerializer,method='POST')
@api_view(['POST'])
def deliverypost(request):
    serializer = SellerDeliverySerializer(data=request.data)
    if serializer.is_valid():
        logistic_service =  serializer.validated_data.get('service')
        order = serializer.validated_data.get('order')
        delivery = Delivery.objects.create(
            order=order, service =logistic_service, receiver=order.user, status="Pr",
            origin=order.seller.address, current=order.seller.address, destination=order.address
        )

        if logistic_service.webhook_url:
            print("Notifying Delivery guy")
            serializer1 = DeliverySerializer(delivery)
            res = requests.request('POST', logistic_service.webhook_url, json=serializer1.data)
        return Response(OrderSerializer(instance=order).data)
    return Response(status=400)
class SellerRegisterView(View):
    def get(self, request):
        form = SellerRegistrationForm()
        return render(request, 'seller/register.html', context={'form': form})

    def post(self, request):
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            seller = form.save()
            return redirect('/seller/login')
        else:
            return render(request, 'seller/register.html', context={'form': form})
