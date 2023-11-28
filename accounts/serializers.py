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
from django.db.models import F


class ProfileSerializer(serializers.ModelSerializer):
    reading_nums = serializers.IntegerField()  # 독해 문제 푼 수
    word_nums = serializers.IntegerField()  # 단어 푼 수
    score = serializers.SerializerMethodField()  # 사용자의 순위 점수(독해 문제 푼 수 + 정답한 단어 수)
    rankers = serializers.SerializerMethodField()  # 닉네임 리스트

    class Meta:
        model = User
        fields = (
            "nickname",
            "email",
            "profile_img",
            "created_at",
            "reading_nums",
            "word_nums",
            "score",
            "rankers",
        )

    # 독해 문제 푼 수와 단어 푼 수를 더하여 순위 점수를 계산
    def get_score(self, obj):
        user_score = obj.reading_nums + obj.word_nums
        return user_score

    # 상위 10명의 사용자를 가져와서 닉네임을 리스트로 변환
    def get_rankers(self, obj):
        top_10_rankers = User.objects.annotate(
            score=F('reading_nums') + F('word_nums')
        ).order_by('-score')[:10]
        return [user.nickname for user in top_10_rankers]


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
