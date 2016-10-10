# -*- encoding: utf-8 -*-
"""Product views."""

from rest_framework import viewsets

from api.models.product import (Product, Keyword, Attribute, ProductAttribute,
                                ProductExtraInfo, ProductLogistic)
from api.serializers.product import (ProductSerializer, KeywordSerializer,
                                     AttributeSerializer,
                                     ProductAttributeSerializer,
                                     ProductExtraInfoSerializer,
                                     ProductLogisticSerializer)


class KeywordViewSet(viewsets.ModelViewSet):
    """Keyword view set."""
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    """Attribute view set."""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """Product attribute view set."""
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Product view set."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductExtraInfoViewSet(viewsets.ModelViewSet):
    """Product extra information view set."""
    queryset = ProductExtraInfo.objects.all()
    serializer_class = ProductExtraInfoSerializer


class ProductLogisticViewSet(viewsets.ModelViewSet):
    """Product logistic view set."""
    queryset = ProductLogistic.objects.all()
    serializer_class = ProductLogisticSerializer
