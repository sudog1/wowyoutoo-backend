from django.urls import path

from accounts import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="Login_View"),
    path("signup/", views.SignupView.as_view(), name="Sign_up_View"),
    # path("dj-rest-auth/", include("dj_rest_auth.urls")),  # 로그인
    # path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
