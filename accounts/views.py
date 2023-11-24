from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from accounts.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import (
    CustomTokenObtainPairSerializer,
    CustomRegisterSerializer,
    ProfileSerializer,
)
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from rest_framework import status, permissions
import os
from rest_framework import status
from .models import User
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.github import views as github_view
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from json.decoder import JSONDecodeError
import json
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import login
from allauth.account.models import EmailConfirmation
from rest_framework_simplejwt.tokens import RefreshToken


class ProfileView(APIView):
    def get(self, request, user_id):
        profile = get_object_or_404(User, id=user_id)
        if request.user.email == profile.email:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, user_id):
        print(request.FILES)
        user = get_object_or_404(User, id=user_id)
        social_user = SocialAccount.objects.filter(
            user=user)  # allauth의 소셜어카운트 모델
        if request.user == user:
            if social_user:  # 소셜 계정일경우, 에러 메세지
                return Response(
                    {"message": "소셜 로그인 사용자는 변경이 불가능합니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if "present_pw" in request.data:  # 비밀번호 변경할 때
                # 현재 비밀번호가 일치하는지 확인.
                if check_password(request.data["present_pw"], user.password) == True:
                    # 새로 입력한 비밀번호와 비밀번호 확인이 일치하는지 확인.
                    if request.data["password"] == request.data["password_check"]:
                        serializer = ProfileSerializer(
                            user,
                            data=request.data,
                            partial=True,  # partial은 전달된 필드 데이터만 부분적으로 사용가능
                        )
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response(
                                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {"message": "비밀번호가 일치하지 않습니다. 다시 입력하세요."},
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response(
                        {"message": "현재 비밀번호를 확인하세요."}, status=status.HTTP_403_FORBIDDEN
                    )

            else:  # 비밀번호 변경안하면 프로필 필드 업데이트 진행
                serializer = ProfileSerializer(
                    user, data=request.data, partial=True)

                if social_user:  # 여기도 소셜 유저일경우 에러 메세지
                    return Response(
                        {"message": "소셜 로그인 사용자는 변경이 불가능합니다."},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                if serializer.is_valid():
                    serializer.save()
                    print(serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class HomeView(APIView):
    def get(self, key):
        return redirect("http://127.0.0.1:5500/login.html")


# dj-rest-auth 이메일 인증 로직
"""
1. 이메일 전송
    제공된 dj_rest_auth.registration.urls로 회원가입시 자동으로 이메일 전송
2. 이메일 확인
    ConfirmEmailView를 활용하여 이메일 확인 로직이 진행
    이메일 확인 키를 추출하고, 해당 키를 사용하여 이메일 확인 객체를 가져옴
3. 이메일 확인 처리
    ConfirmEmailView에서 가져온 이메일 확인 객체의 confirm 메서드를 호출하여 이메일을 확인
    확인에 성공하면, 사용자는 인증된 상태로 간주하고 인증에 실패하면 지정된 경로로 이동시킴
4. 권한 설정
    Allowany로 모든 사용자가 이뷰에 접근할수있게함 
"""


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        # 사용자가 이메일 확인 링크로 GET 요청을 보낼 때 실행되는 메서드
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect("accounts/")  # 인증실패  # 인증성공
        # 이메일 확인 객체를 가져오고, 해당 객체의 confirm 메서드를 호출하여 이메일을 확인

    def get_object(self, queryset=None):
        # URL에서 추출한 이메일 확인 키를 사용하여 EmailConfirmationHMAC.from_key를 호출하여 이메일 확인 객체를 가져옴
        key = self.kwargs["key"]
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return HttpResponseRedirect("accounts/")  # 인증실패 # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        # 모든 유효한 이메일 확인 객체를 반환하는 쿼리셋을 정의
        qs = qs.select_related("email_address__user")
        # 연결된 이메일 주소 및 사용자 정보를 함께 가져움
        return qs


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    # serializer 의 토큰을 커스텀한 토큰키로 봐꿔준다
    # The serializer class that should be used for validating and deserializing input, and for serializing output
    serializer_class = CustomTokenObtainPairSerializer


class Token_Test(APIView):
    def get(self, request):
        print(request.user)
        return Response("get요청")


class KakaoLogin(APIView):
    def post(self, request):
        state = os.environ.get("STATE")
        client_id = os.environ.get("KAKAO_REST_API_KEY")

        received_code = request.data.get("code")  # 받은 ?code='' 값
        code_value = received_code.split("?code=")[-1]  # 코드 값만 추출
        print(code_value)

        kakao_token = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": "http://127.0.0.1:5501/templates/redirect.html",
                "code": code_value,
            },
        )
        print(kakao_token.json)  # access_token 발급 완료
        print("####")

        access_token = kakao_token.json()["access_token"]
        refresh_token = kakao_token.json()["refresh_token"]

        token_data = {"access": access_token, "refresh": refresh_token}
        # access_token 으로 사용자 정보 가져오기
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        # 이메일, 닉네임, 프로필 사진 가져오기
        # print(user_data.json())
        user_data = user_data.json()

        kakao_account = user_data.get("kakao_account")
        user_email = kakao_account.get("email")
        user_nickname = kakao_account.get("profile")["nickname"]
        user_img = kakao_account.get("profile")["profile_image_url"]
        # print(user_email, user_nickname, user_img)

        try:
            # 기존에 가입된 유저나 소셜 로그인 유저가 존재하면 로그인
            user = User.objects.get(email=user_email)
            social_user = SocialAccount.objects.filter(
                user__email=user_email).first()  # 소셜어카운트 모델에는 email field가 없음, User 모델 간에 외래 키 관계가 있다고함 그래서 user__넣음

            # 소셜 로그인 사용자의 경우
            if social_user:
                # 사용자의 비밀번호 없이 로그인 가능한 JWT 토큰 생성
                refresh = RefreshToken.for_user(user)
                # 리프레시 토큰/ 액세스 토큰을 문자열로 변환하여 JSON 형식으로 응답 데이터에 포함시켜 프론트에게 전달
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "로그인 성공"}, status=status.HTTP_200_OK)

            # 동일한 이메일의 유저가 있지만, 소셜 계정이 아닐 때
            if social_user is None:
                return Response({"error": "소셜 계정이 아닌 이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 소셜 계정이 카카오가 아닌 다른 소셜 계정으로 가입했을 때
            if social_user.provider != "kakao":
                return Response({"error": "다른 소셜 계정으로 가입되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 유저 모델에 생성후 소셜어카운트에 포함시키는 로직
            new_user = User.objects.create(
                email=user_email,
                nickname=user_nickname,
                profile_img=user_img,
            )

            # 소셜 계정도 생성하고 포함시키기
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="kakao",
            )

            # 새로운 사용자에 대한 JWT 토큰 생성
            refresh = RefreshToken.for_user(new_user)
            # 리프레시 토큰/ 액세스 토큰을 문자열로 변환하여 JSON 형식으로 응답 데이터에 포함시켜 프론트에게 전달
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "회원가입 성공"}, status=status.HTTP_201_CREATED)


class GithubLogin(APIView):
    def post(self, request):
        state = os.environ.get("STATE")
        client_id = os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")

        received_code = request.data.get("code")
        code_value = received_code.split("?code=")[-1]

        """토큰"""
        github_token = requests.post(
            f"https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_url": "http://127.0.0.1:5501/templates/redirect.html",
                "code": code_value,
            },
        )

        print(github_token.json()["access_token"])
        access_token = github_token.json()["access_token"]

        token_data = {"access": access_token, "auth": "github"}

        """유저 데이터"""
        user_data = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        user_data = user_data.json()

        """유저 이메일"""
        user_emails = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_emails = user_emails.json()

        try:
            user = User.objects.get(email=user_emails[0]["email"])
            social_user = SocialAccount.objects.filter(
                user__email=user_emails[0]["email"]).first()

            if social_user:
                refresh = RefreshToken.for_user(user)

                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "로그인 성공"}, status=status.HTTP_200_OK)

            if social_user is None:
                return Response({"error": "소셜 계정이 아닌 이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

            if social_user.provider != "github":
                return Response({"error": "다른 소셜 계정으로 가입되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            new_user = User.objects.create(
                nickname=user_data.get("login"),
                email=user_emails[0]["email"],
                profile_img=user_data.get("avatar_url")
            )
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="github",
            )

            refresh = RefreshToken.for_user(new_user)

            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "회원가입 성공"}, status=status.HTTP_201_CREATED)
