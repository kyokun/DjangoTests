# -*- coding: utf-8 -*-
"""API urls."""

from django.conf.urls import url, include

from rest_framework import routers

from api.views import (IndustryViewSet, CountryViewSet, StateViewSet,
                       CategoryViewSet)
from api.views.product import (ProductViewSet, KeywordViewSet,
                               AttributeViewSet, ProductAttributeViewSet,
                               ProductExtraInfoViewSet, ProductLogisticViewSet)

router = routers.DefaultRouter()
router.register(r'industries', IndustryViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'keywords', KeywordViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'product_attributes', ProductAttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'products_extra_info', ProductExtraInfoViewSet)
router.register(r'product_logistics', ProductLogisticViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
