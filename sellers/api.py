from rest_framework.routers import DefaultRouter

from sellers import views

router = DefaultRouter()
router.register('seller', views.SellerViewSet, basename='seller')

urlpatterns = [*router.urls]
