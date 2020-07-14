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
