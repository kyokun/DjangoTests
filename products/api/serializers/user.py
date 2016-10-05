# -*- coding: utf-8 -*-
"""User serializers."""

from django.contrib.auth.models import User

from rest_framework import serializers

from api.models.user import UserProfile


def create_user(user_data, profile=None):
    print(user_data)
    user_data['username'] = user_data['email']
    user_data.pop('password_confirmation')
    if profile is not None:
        user = User.objects.create(profile=profile, **user_data)
    else:
        user = User.objects.create(**user_data)
    user.set_password(user_data['password'])
    user.save()
    return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=User._meta.get_field('password').max_length,
        min_length=6)
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'})
    email = serializers.EmailField

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'password',
                  'password_confirmation',)

    def validate_email(self, attrs):
        email = User.objects.filter(email=attrs)
        if email:
            raise serializers.ValidationError('Email address already exists.')
        return attrs

    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError(
                {'password': 'Password confirmation must match Password'})
        return attrs

    def create(self, validated_data):
        return create_user(validated_data)

    def to_representation(self, instance):
        return {'pk': instance.pk, 'first_name': instance.first_name,
                'last_name': instance.last_name, 'email': instance.email}


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    user = UserSerializer(many=False)
    phone = serializers.CharField(min_length=8, max_length=10)

    class Meta:
        model = UserProfile
        fields = ('user', 'phone', 'role',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        profile = UserProfile.objects.create(**validated_data)
        create_user(user_data, profile=profile)
        return profile
