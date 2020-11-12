from django.urls import path

from sellers import views

urlpatterns = [
    path('register', views.SellerRegisterView.as_view(), name='seller_register'),
]
