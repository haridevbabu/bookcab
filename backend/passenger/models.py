from django.db import models

# Create your models here.

"""
Store passenger details
"""
class Passenger(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    mobile = models.IntegerField(unique=True)

class Driver(models.Model):
    """
    Storing driver details
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    mobile = models.IntegerField(unique=True)
    car_no = models.CharField(max_length=80, unique=True)
