"""Serializers for user service"""
from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
