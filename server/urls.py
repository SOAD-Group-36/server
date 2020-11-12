from django.conf import settings
from django.conf.urls.static import serve
from django.contrib import admin
from django.urls import path, include, re_path

from server.swagger import swagger_urls


urlpatterns = (
    [
        path("", include("home.urls")),
        path("", include('users.urls')),
        path("admin/", admin.site.urls),
        path("api/", include("sellers.api")),
        path("api/", include("products.urls")),
        path("api/", include("orders.urls")),
        path("api/", include("delivery.urls")),
        path("seller/", include("sellers.urls")),
    ]
    + swagger_urls
    + [
        # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        re_path(
            r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        ),
    ]
)
