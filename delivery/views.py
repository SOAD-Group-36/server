from django.shortcuts import render
from rest_framework import viewsets, mixins
from delivery import models
from delivery import serializers


class LogisticViewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = models.LogisticServices.objects.all()
    serializer_class = serializers.LogisticSerializer
