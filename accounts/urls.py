from django.urls import path, include
from accounts import views
# from .views import google_login, google_callback, GoogleLogin

urlpatterns = [
    # 구글 소셜로그인
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(),
         name='google_login_todjango'),

    path("dj-rest-auth/", include("dj_rest_auth.urls")),  # 로그인
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
