from django.views import View
from django.shortcuts import render
from django.db.models import Q

from products.models import Product


class HomePage(View):
    def get(self, request):
        products = Product.objects.all()
        if request.GET.get('query', None):
            query = request.GET['query']
            products = products.filter(
                Q(name__contains=query) | Q(description__contains=query) & Q(stock__gt=0)
            )
        context = {'products': products, 'exists': products.count() > 0}
        return render(request, 'home/index.html', context=context)
