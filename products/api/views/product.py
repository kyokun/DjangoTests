# -*- encoding: utf-8 -*-
"""Product views."""

from rest_framework import viewsets

from api.models.product import Product
from api.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Product view set."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
