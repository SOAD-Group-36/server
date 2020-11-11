from django.urls import path, include
from rest_framework import routers
from products import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewset)

urlpatterns = [
    path("product/", include(router.urls)),
]
