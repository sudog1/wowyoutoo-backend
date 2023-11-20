from django.urls import path
from . import views

urlpatterns = [
    # 대화 생성
    # path("dialogue/", views.DialogueView.as_view(), name="dialogue"),
    # 독해퀴즈 생성, 리스트 전체보기
    path("reading/", views.ReadingView.as_view(), name="reading_list"),
    # 리스트에 추가 및 삭제, 독해 다시보기
    path("reading/<quiz_id>/", views.ReadingView.as_view(), name="reading_detail"),
    # db에 단어추가,단어시험보기
    path("word/", views.WordView.as_view(), name="word"),
    # 내 단어장에 단어추가, 제거
    path("wordsbook/<word_id>/", views.WordsBookView.as_view(), name="wordsbook"),
    # 내 단어장 조회
    path("wordsbook/", views.WordsBookView.as_view(), name="wordsbook_list"),
]
