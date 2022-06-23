from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('account/', include('django.contrib.auth.urls')),
  path('', Index.as_view(), name='index'),
  path('about/', About.as_view(), name='about'),
  path('menu/', Menu.as_view(), name='menu'),
  path('menu/search/', MenuSearch.as_view(), name='menu-search'),
  path('order/', Order.as_view(), name='order'),
  path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),name='order-confirmation'),
  path('payment-confirmation/', OrderPayConfirmation.as_view(),name='payment-confirmation'),
]