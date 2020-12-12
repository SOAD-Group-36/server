from auth.permissions import IsLogisticServices
from auth.authentication import LogisticServicesAuthentication
from delivery.forms import LogisticServiceRegistrationForm
from django.shortcuts import redirect, render
from django.views.generic.base import View
from rest_framework import viewsets, mixins
from delivery import models
from delivery import serializers


class LogisticViewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    authentication_classes = (LogisticServicesAuthentication,)
    permission_classes = (IsLogisticServices,)
    queryset = models.LogisticServices.objects.all()
    serializer_class = serializers.LogisticSerializer


class DeliveryViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (LogisticServicesAuthentication,)
    permission_classes = (IsLogisticServices,)
    queryset = models.Delivery.objects.all()
    serializer_class = serializers.DeliverySerializer


class LogisticServiceRegisterView(View):
    def get(self, request):
        form = LogisticServiceRegistrationForm()
        return render(request, 'seller/register.html', context={'form': form})

    def post(self, request):
        form = LogisticServiceRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            seller = form.save()
            return redirect('/seller/login')
        else:
            return render(request, 'seller/register.html', context={'form': form})
