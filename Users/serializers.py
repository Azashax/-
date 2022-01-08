from django.db.models import fields
from rest_framework import serializers
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=256,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('token',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return super(UserProfileSerializer, self).update(instance, validated_data)

    class Meta:
            model = UserProfile
            fields = '__all__'


class AllUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RefreshSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

