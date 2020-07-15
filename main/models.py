from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    types = [
        ('FU', 'fundacja'),
        ('OP', 'organizacja porządkowa'),
        ('ZL', 'zbiórka lokalna')
    ]
    type = models.CharField(max_length=2, choices=types, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=32)  # ulica + nr domu
    phone_number = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256, null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
