# -*- coding: utf-8 -*-
"""Static models."""

from django.db import models


class Industry(models.Model):
    """Industry model."""
    name = models.CharField(max_length=32)


class Country(models.Model):
    """Country model."""
    phone_code = models.CharField(max_length=5, null=True)
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)


class State(models.Model):
    """State model."""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=2)


class Category(models.Model):
    """Category model."""
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
