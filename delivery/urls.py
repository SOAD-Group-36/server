from django.urls import path, include
from rest_framework import routers
from delivery import views

router = routers.DefaultRouter()
router.register(r'Logisticservices', views.LogisticViewset)

urlpatterns = [
    path("logisticservices/", include(router.urls)),
]
