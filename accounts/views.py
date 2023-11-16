from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from accounts.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenObtainPairSerializer, CustomRegisterSerializer
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


state = os.environ.get("STATE")
BASE_URL = 'http://localhost:5500/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/social/kakao/'
GITHUB_CALLBACK_URI = BASE_URL + 'accounts/social/github'


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


# class SignupView(APIView):
#     def post(self, request):
#         # 사용자 정보를 받아서 회원을 생성합니다.
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message ": "가입완료!"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                 {"massage": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
#             )

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


def kakao_login(self, request):
    code = request.data.get("code")
    access_token = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "client_id": os.environ.get("KAKAO_REST_API_KEY"),
            "redirect_uri": KAKAO_CALLBACK_URI,
            "code": code
        },
    )
    access_token = access_token.json().get("access_token")

    user_data = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )
    user_data = user_data.json()

    kakao_account = user_data.get("kakao_account")
    profile = kakao_account.get("profile")
    try:
        user = User.objects.get(email=kakao_account.get("email"))
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        user = User.objects.create(
            email=kakao_account.get("email"),
            username=profile.get("nickname"),
            name=profile.get("nickname"),
            avatar=profile.get("profile_image_url"),
        )
        user.set_unusable_password()
        user.save()
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""Kakao 로그인 호출:
Kakao 로그인을 구현하기 위해 필요한 REST API 키를 얻고
사용자를 Kakao 인증 화면으로 리디렉션하는 URL을 생성"""


# def kakao_login(request):
#     rest_api_key = os.environ.get('KAKAO_REST_API_KEY')
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
#     )


"""Kakao 콜백 처리:
Kakao에서 제공하는 콜백 URL에서는 인가 코드를 받아오고
받아온 인가 코드를 사용하여 Kakao로부터 액세스 토큰을 요청."""


# def kakao_callback(request):

#     rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
#     code = request.GET.get("code")
#     redirect_uri = KAKAO_CALLBACK_URI

#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")

#     # 에러 발생 시 종료
#     if error is not None:
#         raise JSONDecodeError(error)

#     # access_token 가져오기
#     access_token = token_req_json.get('access_token')

#     # 카카오톡 프로필, 배경 이미지 url, 이메일 가져올수있음
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
#     profile_json = profile_request.json()
#     error = profile_json.get("error")

#     if error is not None:
#         raise JSONDecodeError(error)
#     kakao_account = profile_json.get('kakao_account')
#     email = kakao_account.get('email')
#     nickname = kakao_account.get('nickname')

#     """사용자 처리 및 응답:
#     Kakao로부터 받아온 사용자 프로필 정보를 로컬 데이터베이스에서 사용자를 확인하고 처리
#     처리 결과에 따라 로그인 또는 회원가입을 수행하고, 결과를 JSON 형식으로 반환"""

#     try:
#         user = User.objects.get(email=email)
#         # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse({'err_msg': '이미 존재하는 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'kakao':
#             return JsonResponse({'err_msg': '카카오 메일에 등록되지않은 계정입니다.'}, status=status.HTTP_400_BAD_REQUEST)

#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': '로그인에 실패하셨습니다.'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#     except User.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': '회원가입에 실패하셨습니다.'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)


# class KakaoLogin(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI


def github_login(request):
    client_id = os.environ.get('SOCIAL_AUTH_GITHUB_CLIENT_ID')
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={GITHUB_CALLBACK_URI}&scope=read:user user:email"
    )


def github_callback(request):

    client_id = os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID")
    client_secret = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')
    code = request.GET.get("code")

    """토큰"""
    token_data = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}&response_type=code", headers={'Accept': 'application/json'})
    token_data_json = token_data.json()
    error = token_data_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_data_json.get('access_token')

    """유저 데이터"""
    user_data = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )

    user_data = user_data.json()
    print(user_data)
    user_emails = requests.get(
        "https://api.github.com/user/emails",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    user_emails = user_emails.json()
    print(user_emails)
    try:
        user = User.objects.get(email=user_emails[0]["email"])
        # user = User.objects.get(nickname=nickname)
        print(user)
        return JsonResponse({'message': '사용자가 성공적으로 로그인되었습니다'}, status=200)
    except User.DoesNotExist:
        user = User.objects.create(
            nickname=user_data.get("login"),
            email=user_emails[0]["email"],
            profile_img=user_data.get("avatar_url"),
        )
        user.set_unusable_password()    # password 없음
        user.save()

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        print(data)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    #     return JsonResponse({'message': '새로운 사용자가 생성되었고 로그인되었습니다'}, status=200)
    # except Exception:
    #     return JsonResponse({'error': 'GitHub 콜백 처리에 실패했습니다'}, status=400)

    # try:
    #     user = User.objects.get(email=email)
    #     # 기존에 가입된 유저의 Provider가 github가 아니면 에러 발생, 맞으면 로그인
    #     # 다른 SNS로 가입된 유저
    #     social_user = SocialAccount.objects.get(user=user)
    #     if social_user is None:
    #         return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
    #     if social_user.provider != 'github':
    #         return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
    #     # 기존에 github로 가입된 유저
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(
    #         f"{BASE_URL}accounts/github/login/finish/", data=data)
    #     accept_status = accept.status_code
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
    # except User.DoesNotExist:
    #     # 기존에 가입된 유저가 없으면 새로 가입
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(
    #         f"{BASE_URL}accounts/github/login/finish/", data=data)
    #     accept_status = accept.status_code
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
    #     # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)


class GithubLogin(SocialLoginView):
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client
