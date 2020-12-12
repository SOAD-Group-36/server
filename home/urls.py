from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('orders', views.OrderHistoryView.as_view(), name='orders'),
    path('product/<product_id>', views.ProductDetailView.as_view(), name='product'),
    path('order/<product_id>', views.ProductOrderPlaceView.as_view(), name='place_order'),
]
