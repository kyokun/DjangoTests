# -*- coding: utf-8 -*-
"""API urls."""

from django.conf.urls import url, include

from rest_framework import routers

from api.views import (IndustryViewSet, CountryViewSet, StateViewSet,
                       CategoryViewSet, UserProfileViewSet)
from api.views.company import CompanyViewSet

router = routers.DefaultRouter()
router.register(r'industries', IndustryViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
