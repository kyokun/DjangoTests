# -*- coding: utf-8 -*-
"""Company serializers."""

from rest_framework import serializers

from api.models.static import Country, State
from api.models.company import Company


class AddressSerializer(serializers.ModelSerializer):
    """Address serializer."""
    class Meta:
        model = Company
        fields = ('street', 'country', 'num_ext', 'zip_code', 'state',)


class MainPhoneSerializer(serializers.Serializer):
    """Main phone serializer."""
    number = serializers.CharField(source='phone_number')
    name = serializers.CharField(source='phone_name')
    extension = serializers.CharField(source='phone_extension')
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='phone_country')


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer."""
    address = AddressSerializer(source='*')
    main_phone = MainPhoneSerializer(source='*')

    class Meta:
        model = Company
        fields = ('id', 'business_name', 'website', 'industry',
                  'product_categories', 'address', 'main_phone',)

    def create(self, validated_data):
        categories = validated_data.pop('product_categories')
        company = Company.objects.create(**validated_data)
        for category in categories:
            company.product_categories.add(category)
        company.save()
        return company
