from django.urls import path
from . import views


urlpatterns = [
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
]