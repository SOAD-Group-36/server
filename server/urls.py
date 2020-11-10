from django.contrib import admin
from django.urls import path, include

from server.swagger import swagger_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sellers.urls")),
    path("api/", include("products.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("delivery.urls")),
] + swagger_urls
