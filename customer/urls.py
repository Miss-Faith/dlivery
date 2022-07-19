from django.urls import path,include
from .views import *

urlpatterns = [
  path('', Index, name='index'),
  path('social-auth/', include('social_django.urls', namespace='social')),
  path('about/', About, name='about'),
  path('menu/', Menu.as_view(), name='menu'),
  path('menu/search/', MenuSearch.as_view(), name='menu-search'),
  path('order/', Order.as_view(), name='order'),
  path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),name='order-confirmation'),
  path('payment-confirmation/', OrderPayConfirmation.as_view(),name='payment-confirmation'),
]