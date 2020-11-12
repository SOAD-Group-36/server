from django.shortcuts import render, redirect
from django.views import View
from rest_framework import mixins
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from sellers.forms import SellerRegistrationForm
from sellers.models import Seller
from sellers.serializers import SellerSerializer


class SellerViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


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
