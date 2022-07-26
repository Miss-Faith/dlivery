from django.urls import path,include
from django.conf.urls import url
# from django.urls import re_path as url
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import *

urlpatterns = [
  path('', Index, name='index'),
  path('register/', RegisterView.as_view(), name='users-register'),
  path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html', authentication_form=LoginForm), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
  
  path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
  path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
  path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

  url(r'^oauth/', include('social_django.urls', namespace='social')),

  path('profile/', profile, name='users-profile'),
  
  path('about/', About, name='about'),
  path('menu/', Menu.as_view(), name='menu'),
  path('menu/search/', MenuSearch.as_view(), name='menu-search'),
  path('order/', Order.as_view(), name='order'),
  path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),name='order-confirmation'),
  path('payment-confirmation/', OrderPayConfirmation.as_view(),name='payment-confirmation'),
]