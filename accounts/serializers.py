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


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs[self.username_field])

        if check_password(attrs['password'], user.password) == False:
            raise NotFound("사용자를 찾을 수 없습니다. 로그인 정보를 확인하세요.")  # 404 Not Found
        # elif user.is_active == False:
        #     raise AuthenticationFailed("이메일 인증이 필요합니다.")  # 401 Unauthorized
        else:
            # 기본 동작을 실행하고 반환된 데이터를 저장합니다.
            data = super().validate(attrs)
            return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        return token
