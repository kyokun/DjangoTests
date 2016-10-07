# -*- coding: utf-8 -*-
"""Company views."""

from rest_framework import viewsets

from api.models.company import Company
from api.serializers.company import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """Company view set."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
