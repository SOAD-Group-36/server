from django.urls import path, include
from rest_framework import routers
from orders import views

router = routers.DefaultRouter()
router.register(r'Orders', views.OrderViewset)

urlpatterns = [
    path("orders/", include(router.urls)),
]
