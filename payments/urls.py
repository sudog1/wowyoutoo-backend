from django.urls import path
from . import views

urlpatterns = [
    # 결제 전 검증을 위한 결제 정보 DB 저장
    path("prepare/", views.PrepareView.as_view(), name="prepare"),
    # 결제 결과 검증을 위한 실 결제 금액과 결제요청금액을 비교
    path("complete/", views.CompleteView.as_view(), name="complete"),
]