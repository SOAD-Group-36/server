from django.views import View
from django.shortcuts import render

from products.models import Product


class HomePage(View):
    def get(self, request):
        context = {'products': Product.objects.all()}
        return render(request, 'home/index.html', context=context)
