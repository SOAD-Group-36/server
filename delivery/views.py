from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import viewsets, mixins
from delivery import models
from delivery import serializers


class LogisticViewset(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = models.LogisticServices.objects.all()
    serializer_class = serializers.LogisticSerializer


class LogisticServiceRegisterView(View):
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
