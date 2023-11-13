from rest_framework import serializers
from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    """ 회원가입 페이지"""
    # 이메일 중복 검증
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token['username'] = user.username

        # ...

        return token
