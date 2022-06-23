from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
]