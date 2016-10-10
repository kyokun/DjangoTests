# -*- coding: utf-8 -*-
"""Product models."""

from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from api.models import Country, Category


class Keyword(models.Model):
    """Keyword model."""
    name = models.CharField(max_length=128)


class Attribute(models.Model):
    """Attribute model."""
    name = models.CharField(max_length=64)


class ProductAttribute(models.Model):
    """Product attribute model."""
    value = models.CharField(max_length=128)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    price = models.PositiveIntegerField()
    made_in = models.ForeignKey(Country, on_delete=models.CASCADE)
    last_modification = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    keywords = models.ManyToManyField(Keyword)
    attributes = models.ManyToManyField(ProductAttribute)


class ProductExtraInfo(models.Model):
    """Product extra information model"""
    title = models.CharField(max_length=128)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductLogistic(models.Model):
    """Product logistic model."""
    origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    PERIOD_CHOICES = (
        ('D', 'Day'),
        ('M', 'Month'),
        ('Y', 'Year'),
        ('W', 'Week'),
    )
    period = models.CharField(choices=PERIOD_CHOICES, default='W',
                              max_length=10)
    product = models.ForeignKey(Product)


@receiver(signals.post_save, sender=Product)
def save_product(sender, instance, update_fields, created, **kwargs):
    if created:
        ProductExtraInfo.objects.create(product=instance)
