from django.urls import path
from . import views

urlpatterns = [
    # 독해문제 생성, 기존 독해문제 리스트
    path("reading/", views.ReadingView.as_view(), name="reading_list"),
    # 리스트에 추가 및 삭제, 독해 다시보기
    path("reading/<quiz_id>/", views.ReadingView.as_view(), name="reading_detail"),
    # 복습노트에서 독해문제 리스트 가져오기,
    path("readingbook/", views.ReadingBookView.as_view(), name="readingbook_list"),
    # 복습노트에 독해문제 저장, 독해문제 상세 보기
    path(
        "readingbook/<quiz_id>/", views.ReadingView.as_view(), name="readingbook_detail"
    ),
    # db에 단어추가,단어시험보기
    path("word/", views.WordView.as_view(), name="word"),
    # 내 단어장에 단어추가, 제거
    path("wordsbook/<word_id>/", views.WordsBookView.as_view(), name="wordsbook"),
    # 내 단어장 조회
    path("wordsbook/", views.WordsBookView.as_view(), name="wordsbook_list"),
]
