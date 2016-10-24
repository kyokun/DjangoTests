# -*- encoding: utf-8 -*-
"""Product serializers."""

from rest_framework import serializers

from api.models import (ProductAttribute, Attribute, ProductExtraInfo,
                        Keyword, Product, ProductLogistic)


class KeywordSerializer(serializers.ModelSerializer):
    """Keyword serializer."""
    class Meta:
        model = Keyword
        fields = ('name',)

    def create(self, validated_data):
        return Keyword.objects.get_or_create(name=validated_data['name'])[0]

    def to_representation(self, instance):
        return instance.name


class AttributeSerializer(serializers.ModelSerializer):
    """Attribute serializer."""
    class Meta:
        model = Attribute
        fields = ('name',)

    def create(self, validated_data):
        return Attribute.objects.get_or_create(name=validated_data['name'])[0]


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Product attribute serializer."""
    name = serializers.CharField(
        max_length=Attribute._meta.get_field('name').max_length
    )

    class Meta:
        model = ProductAttribute
        fields = ('name', 'value',)

    def create(self, validated_data):
        value = validated_data.pop('value').lower()
        attribute = AttributeSerializer().create(validated_data)
        return ProductAttribute.objects.get_or_create(
            attribute=attribute, value=value)[0]

    def to_representation(self, instance):
        return {
            'name': instance.attribute.name,
            'value': instance.value
        }


class ProductExtraInfoSerializer(serializers.ModelSerializer):
    """Product extra information serializer."""
    class Meta:
        model = ProductExtraInfo
        fields = ('title', 'description',)


class ProductLogisticSerializer(serializers.ModelSerializer):
    """Product logistic serializer."""
    class Meta:
        model = ProductLogistic
        fields = ('origin', 'quantity', 'period',)
        extra_kwargs = {
            'origin': {'write_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""
    keywords = KeywordSerializer(many=True)
    attributes = ProductAttributeSerializer(many=True)
    extras = ProductExtraInfoSerializer(many=True, required=False)
    logistics = ProductLogisticSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'brand', 'price', 'made_in',
                  'category', 'keywords', 'attributes', 'extras', 'logistics')

    def create(self, validated_data):
        keywords = validated_data.pop('keywords')
        attributes = validated_data.pop('attributes')
        product = Product.objects.create(**validated_data)
        for keyword in keywords:
            keyword = KeywordSerializer().create(keyword)
            product.keywords.add(keyword)
        for attribute in attributes:
            attribute = ProductAttributeSerializer().create(attribute)
            product.attributes.add(attribute)
        return product

    def update(self, instance, validated_data):
        if validated_data.get('extras'):
            extras = validated_data.pop('extras')
            for extra in extras:
                ProductExtraInfo.objects.create(product=instance, **extra)
        if validated_data.get('logistics'):
            logistics = validated_data.pop('logistics')
            for logistic in logistics:
                ProductLogistic.objects.create(product=instance, **logistic)
        return instance

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        extras = instance.extras.count() != 0
        logistics = instance.logistics.count() != 0
        data.update({'flags': {
            'complete': extras and logistics,
            'extras': extras,
            'logistics': logistics
        }})
        return data
