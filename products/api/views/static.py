# -*- coding: utf-8 -*-
""" Static views """

from rest_framework import viewsets

from api.models import Industry, Country, State, Category
from api.serializers import (IndustrySerializer, CountrySerializer,
                             StateSerializer, CategorySerializer)


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
