from django.urls import path
from delivery import views


urlpatterns = [
    path('register', views.LogisticServiceRegisterView.as_view(), name='delivery_register'),
]
