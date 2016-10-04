# -*- coding: utf-8 -*-
"""User models."""

from django.conf import settings
from django.db import models

from api.models import Country


class UserType(models.Model):
    """User type."""
    name = models.CharField(max_length=30)


class UserProfile(models.Model):
    """User profile."""
    role = models.CharField(max_length=32)
    phone = models.CharField(max_length=10)
    phone_country = models.ForeignKey(Country, default=1,
                                      on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE,
                                  default=1)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True, related_name='profile',
                                on_delete=models.CASCADE)
