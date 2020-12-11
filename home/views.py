import requests
from orders.models import Order
from orders.serializers import OrderSerializer
from home.forms import OrderPlaceForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.http import Http404
from django.db.models import Q

from products.models import Product


class HomePage(View):
    def get(self, request):
        products = Product.objects.all()
        if request.GET.get('query', None):
            query = request.GET['query']
            products = products.filter(
                (Q(name__contains=query) | Q(description__contains=query)) & Q(stock__gt=0)
            )
        context = {'products': products, 'exists': products.count() > 0}
        return render(request, 'home/index.html', context=context)


class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Http404()
        context = {'product': product, 'form': OrderPlaceForm()}
        return render(request, 'home/product.html', context=context)

class ProductOrderPlaceView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        return redirect('home:product', product_id=product_id)
    
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Http404()
        form = OrderPlaceForm(request.POST)
        if form.is_valid():
            address, quantity = form.cleaned_data.get('address'), form.cleaned_data.get('quantity')
            user = request.user
            price = product.price * quantity
            order = Order.objects.create(user=user, address=address, quantity=quantity, product=product, price=price)

            # Notify Seller
            if product.seller.webhook_url:
                print("Notifying Seller")
                serializer = OrderSerializer(order)
                res = requests.request('POST', product.seller.webhook_url, json=serializer.data)
            
            return redirect('home:home')
        print(form.errors)
        return render(request, 'home/product.html', context={'product': product, 'form': form})
