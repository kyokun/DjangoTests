# -*- coding: utf-8 -*-
"""User serializers."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from api.models.user import UserProfile


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
        validated_data['username'] = validated_data['email']
        validated_data.pop('password_confirmation')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        return {'pk': instance.pk, 'first_name': instance.first_name,
                'last_name': instance.last_name, 'email': instance.email}


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(write_only=True, max_length=User._meta.get_field('first_name').max_length)
    last_name = serializers.CharField(write_only=True, max_length=User._meta.get_field('last_name').max_length)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6,
                                     max_length=User._meta.get_field('password').max_length,
                                     style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'})
    phone = serializers.CharField(min_length=8, max_length=10)

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'last_name', 'email', 'password', 'password_confirmation', 'phone', 'role',)

    def create(self, validated_data):
        user = dict()
        user['first_name'] = validated_data.pop('first_name')
        user['last_name'] = validated_data.pop('last_name')
        user['email'] = validated_data.pop('email')
        user['password'] = validated_data.pop('password')
        user['password_confirmation'] = validated_data.pop('password_confirmation')
        profile = UserProfile(**validated_data)
        user['profile'] = profile
        serializer = UserSerializer(data=user)

        if serializer.is_valid():
            serializer.save()
            profile.save()
            return profile
        else:
            raise serializers.ValidationError(serializer.errors)

    def to_representation(self, instance):
        try:
            user = instance.user
            return {
                'first_name': user.first_name, 'last_name': user.last_name,
                'email': user.email, 'phone': instance.phone,
                'role': instance.role, 'id': instance.pk
            }
        except ObjectDoesNotExist:
            return {
                'id': instance.pk, 'phone': instance.phone, 'role': instance.role
            }
