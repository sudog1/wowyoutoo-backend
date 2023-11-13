from django.urls import path
from . import views

urlpatterns = [
    # 대화 생성
    path("dialogue/", views.DialogueView.as_view(), name="dialogue"),
    # 지문 생성
    path("passage/create/", views.PassageCreateView.as_view(), name="passage_create"),
    # 내 지문리스트에 저장,내 지문리스트 보기
    path("passage/", views.PassageView.as_view(), name="passage"),
    # 지문 리스트에서 특정지문보기,특정지문삭제
    path("passage/<passage_id>/", views.PassageView.as_view(), name="passage_detail"),
    # db에 단어추가,단어시험보기
    path("word/", views.WordView.as_view(), name="word"),
    # 내 단어장에 단어추가
    path("word/<word_id>/", views.WordsBookView.as_view(), name="append_word"),
    # 내 단어장 조회
    path("<user_id>/word/", views.WordsBookView.as_view(), name="wordsbook"),
    # 내 단어장에서 단어제거
    path(
        "<user_id>/word/<word_id>/", views.WordsBookView.as_view(), name="delete_word"
    ),
]
