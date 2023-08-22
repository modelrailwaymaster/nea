from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class listing(models.Model):
    latest_price = models.DecimalField(max_digits=100, decimal_places=2)
    link = models.CharField(max_length=200)
    website = models.CharField(max_length=250)


class user_saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    wanted_price = models.DecimalField(max_digits=100, decimal_places=2)
