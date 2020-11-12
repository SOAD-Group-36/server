from django.shortcuts import render
from rest_framework import viewsets, mixins
from . import models
from . import serializers


class OrderViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
