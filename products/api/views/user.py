# -*- coding: utf-8 -*-
"""User views."""
from django.contrib.auth.models import User

from rest_framework import viewsets

from api.models.user import UserProfile
from api.serializers.user import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User view set."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile view set."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
