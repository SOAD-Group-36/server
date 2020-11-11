from django.shortcuts import render
from rest_framework import viewsets, mixins
from . import models
from . import serializers


class LogisticViewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = models.LogisticServices.objects.all()
    serializer_class = serializers.LogisticSerializer
