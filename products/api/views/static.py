# -*- coding: utf-8 -*-
"""Static views."""

from rest_framework import viewsets

from api.models import Industry, Country, State, Category
from api.serializers import (IndustrySerializer, CountrySerializer,
                             StateSerializer, CategorySerializer)


class IndustryViewSet(viewsets.ModelViewSet):
    """Industry view set."""
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    """Country view set."""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ModelViewSet):
    """State view set."""
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Category view set."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
