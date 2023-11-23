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
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction


class ProfileSerializer(serializers.ModelSerializer):
    reading_nums = serializers.IntegerField()
    word_nums = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "nickname",
            "email",
            "profile_img",
            "created_at",
            "reading_nums",
            "word_nums",
        )


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.nickname = self.data.get("nickname")
        user.save()
        return user


# class UserSerializer(serializers.ModelSerializer):

#     """ 회원가입 페이지"""
#     # 이메일 중복 검증
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator]
#     )

#     username = serializers.CharField(
#         required=True,
#         validators=[UniqueValidator]
#     )

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password]
#     )

#     class Meta:
#         model = User
#         fields = ("nickname", "password", "email")

#     def create(self, validated_data):
#         user = super().create(validated_data)
#         password = user.password
#         user.set_password(password)
#         user.save()
#         return user

#     def update(self, instance, validated_data):
#         password = validated_data.pop("password", None)
#         if password is not None:
#             instance.set_password(password)
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email

        # ...

        return token
