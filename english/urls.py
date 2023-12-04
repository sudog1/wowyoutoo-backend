from django.urls import path
from . import views

urlpatterns = [
    # 독해문제 생성
    path("reading/new/", views.CreateReadingView.as_view(), name="new_reading"),
    # 기존 독해문제 풀기, 푼 독해문제 카운트
    path("reading/", views.ReadingView.as_view(), name="reading_list"),
    # 복습노트에서 독해문제 리스트 가져오기,
    path("readingbook/", views.ReadingBookView.as_view(), name="readingbook_list"),
    # 복습노트에 독해문제 저장, 제거, 독해문제 상세 보기
    path(
        "readingbook/<quiz_id>/",
        views.ReadingBookView.as_view(),
        name="readingbook_detail",
    ),
    # db에 단어추가,단어시험보기
    path("word/", views.WordView.as_view(), name="add_word"),
    # 푼 단어퀴즈 카운트
    path("word/<word_id>/", views.WordView.as_view(), name="word_count"),
    # 내 단어장 조회
    path("wordsbook/", views.WordsBookView.as_view(), name="wordsbook_list"),
    # 내 단어장에 단어추가, 제거
    path("wordsbook/<word_id>/", views.WordsBookView.as_view(), name="wordsbook"),
]
