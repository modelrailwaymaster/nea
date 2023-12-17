from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class listing(models.Model):
    name = models.CharField(max_length=250, default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    currency = models.CharField(max_length=250, default=0)
    url = models.CharField(max_length=200, default=0)
    location = models.CharField(max_length=250, default=0)
    image = models.CharField(max_length=250, default=0)
    review = models.CharField(max_length=250, default=0)
    website = models.CharField(max_length=250, default=0)


class user_saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    wanted_price = models.DecimalField(max_digits=100, decimal_places=2)
