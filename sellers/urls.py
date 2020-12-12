from django.urls import path,include
from sellers import views
from rest_framework import routers


urlpatterns = [
    path('register', views.SellerRegisterView.as_view(), name='seller_register'),
]