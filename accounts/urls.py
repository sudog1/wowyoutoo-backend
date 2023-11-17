from django.urls import path, include, re_path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.registration.views import VerifyEmailView
# from .views import google_login, google_callback, GoogleLogin

urlpatterns = [
    path('kakao/login/', views.KakaoLogin.as_view(), name='kakao_login'),

    path('github/login/', views.GithubLogin.as_view(), name='github_login'),

    path("signup/", views.CustomRegisterView.as_view(), name="signup"),  # 회원가입
    path("dj-rest-auth/", include("dj_rest_auth.urls")),  # 로그인
    re_path(r"^account-confirm-email/$", VerifyEmailView.as_view(), name="account_email_verification_sent",
            ),
    re_path(r"^account-confirm-email/(?P<key>[-:\w]+)/$", views.ConfirmEmailView.as_view(), name="account_confirm_email",
            ),
    path("api/token/", views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair",),

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
