from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image', blank=False,)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=200, blank=True)
    number = PhoneNumberField(null = True, blank = False)
    address = map_fields.AddressField(max_length=1000, null=True)
    houseno = models.CharField(max_length=200, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'