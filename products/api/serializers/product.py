# -*- encoding: utf-8 -*-
"""Product serializers."""

from rest_framework import serializers

from api.models.product import (Product, Keyword, Attribute, ProductAttribute,
                                ProductExtraInfo, ProductLogistic)


class KeywordSerializer(serializers.ModelSerializer):
    """Keyword serializer."""

    class Meta:
        model = Keyword
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    """Attribute serializer."""

    class Meta:
        model = Attribute
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Product attribute serializer."""

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductExtraInfoSerializer(serializers.ModelSerializer):
    """Product extra information serializer."""

    class Meta:
        model = ProductExtraInfo
        fields = '__all__'
        read_only_fields = ('product',)


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""
    extra_info = ProductExtraInfoSerializer(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'brand', 'price', 'made_in',
                  'category', 'keywords', 'attributes', 'extra_info',)

    def validate_price(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError('Value must be greater than 0')
        return attrs

    def create(self, validated_data):
        extra_info_data = validated_data.pop('extra_info')
        keywords = validated_data.pop('keywords')
        attributes = validated_data.pop('attributes')
        product = Product.objects.create(**validated_data)
        for keyword in keywords:
            product.keywords.add(keyword)
        for attribute in attributes:
            product.attributes.add(attribute)
        extra_info = ProductExtraInfo.objects.get(product_id=product.id)
        extra_info.title = extra_info_data.get('title')
        extra_info.description = extra_info_data.get('description')
        extra_info.save(update_fields=['title', 'description'])
        return product


class ProductLogisticSerializer(serializers.ModelSerializer):
    """Product logistic serializer."""

    class Meta:
        model = ProductLogistic
        fields = '__all__'

    def validate_quantity(self, attrs):
        if attrs < 1:
            raise serializers.ValidationError(
                'Value must be greater or equal than 1'
            )
        return attrs
