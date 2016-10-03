# -*- coding: utf-8 -*-
""" Static serializers. """

from rest_framework import serializers

from api.models import Country, Category, Industry, State


class IndustrySerializer(serializers.ModelSerializer):
    """Industry serializer."""
    class Meta:
        model = Industry
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """Country serializer."""
    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    """State serializer."""
    class Meta:
        model = State
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    class Meta:
        model = Category
        fields = '__all__'
