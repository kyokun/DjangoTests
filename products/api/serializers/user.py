# -*- coding: utf-8 -*-
"""User serializers."""

from django.contrib.auth.models import User

from rest_framework import serializers

from api.models.user import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=User._meta.get_field('password').max_length,
        min_length=6, write_only=True)
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
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
        validated_data['username'] = validated_data['email']
        validated_data.pop('password_confirmation')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])
        return user


class UserProfileSerializer(UserSerializer):
    """User profile serializer."""
    first_name = serializers.CharField(
        max_length=User._meta.get_field('first_name').max_length)
    last_name = serializers.CharField(
        max_length=User._meta.get_field('last_name').max_length)
    email = serializers.EmailField()
    phone = serializers.CharField(min_length=8, max_length=10)

    class Meta:
        model = UserProfile
        fields = UserSerializer.Meta.fields + ('phone', 'role',)

    def create(self, validated_data):
        profile_data = {}
        profile_data['phone'] = validated_data.pop('phone')
        profile_data['role'] = validated_data.pop('role')
        user = super(UserProfileSerializer, self).create(validated_data)
        user.profile.role = profile_data['role']
        user.profile.phone = profile_data['phone']
        user.profile.save(update_fields=['role', 'phone'])
        return user.profile

    def to_representation(self, instance):
        return {
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
            'phone': instance.phone,
            'role': instance.role
        }
