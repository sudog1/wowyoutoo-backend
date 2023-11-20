from django.urls import path
from . import views

urlpatterns = [
    #공지사항 리스트보기.공지사항 특정글보기,공지사항작성,삭제,수정
    path("",views.AnnouncementView.as_view(),name='service'),
    path("<int:announcement_id>/",views.AnnouncementView.as_view(),name='announcement'),
    path("qna/",views.QnaView.as_view(),name='faq'),
    path('qna/<int:qna_id>/',views.QnaView.as_view(),name='faq_detail'),
    path("qna/<int:qna_id>/response/",views.QnaResponseView.as_view(),name='faq_response'),
    path("ad_mail/",views.BackOfficeView.as_view(),name="admail"),
]