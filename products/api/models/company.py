# -*- coding: utf-8 -*-
"""Company models."""

from django.db import models

from api.models import Country, Industry, Category, State


class Company(models.Model):
    """Company model."""
    business_name = models.CharField(max_length=64, unique=True)
    website = models.URLField(max_length=32, blank=True)

    street = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=8)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=10)
    phone_name = models.CharField(max_length=50)
    phone_extension = models.CharField(max_length=5)
    phone_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    product_categories = models.ManyToManyField(Category)
