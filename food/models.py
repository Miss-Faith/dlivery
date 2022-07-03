from django.db import models

# Create your models here.
class Restaurants (models.Model):
  name = models.CharField(max_length=100, primary_key=True, unique=True, blank=False)
  email = models.EmailField(max_length=200, blank=False)
  category = models.TextChoices('Fast Food','Cafe')
  description = models.TextField(max_length=500, blank=True)