from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('business/login', views.BusinessLoginView.as_view(), name='business_login'),
    path('business/api_keys', views.APIKeyGenerateView.as_view(), name='api_keys'),
    path('business/delete_api_key/<api_key>', views.DeleteAPIKey.as_view(), name='delete_api'),
]
