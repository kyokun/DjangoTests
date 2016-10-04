# -*- coding: utf-8 -*-
"""User serializers."""

from django.contrib.auth.models import User

from rest_framework import serializers

from api.models.user import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    password = serializers.CharField(style={'input_type': 'password'})
    password_confirmation = serializers.CharField(
        max_length=User._meta.get_field('password').max_length,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'password',
                  'password_confirmation',)

    def validate(self, attrs):
        password_length = len(attrs['password'])
        if password_length < 6:
            raise serializers.ValidationError({
                'password': 'Password length must be greater than or '
                            'equal to 6.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create(**validated_data)
        return user

    def to_representation(self, instance):
        return {'pk': instance.pk, 'first_name': instance.first_name,
                'last_name': instance.last_name}


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'phone', 'role',)

    def validate(self, attrs):
        phone_length = len(attrs['phone'])
        if phone_length < 8 or phone_length > 10:
            raise serializers.ValidationError({
                'phone': 'Phone length must be greater than or equal '
                         'to 8 and less than or equal to 10.'})
        password = attrs['user']['password']
        password_confirmation = attrs['user']['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError(
                {'password': 'Password confirmation must match Password'})
        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username'] = User.objects.count() + 1
        user_data.pop('password_confirmation')
        profile = UserProfile.objects.create(**validated_data)
        user = User.objects.create(profile=profile, **user_data)
        user.set_password(user_data['password'])
        user.save()
        return profile
