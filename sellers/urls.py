from django.urls import path
from sellers import views

urlpatterns = [
    path("seller", views.SellerCreateView.as_view(), name="seller_create"),
]
