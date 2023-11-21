from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ReadingQuiz
from rest_framework import status
from .constants import content
from openai import OpenAI
import json
from config.settings import OPENAI_API_KEY
from .models import Word, ReadingQuiz, Level
from .serializers import WordQuizesSerializer, WordSerializer, ReadingQuizSerializer
from deep_translator import (
    GoogleTranslator,
    DeeplTranslator,
)

client = OpenAI(api_key=OPENAI_API_KEY)


# Create your views here.
class PassageCreateView(APIView):
    def post(self, request):
        pass


class ReadingView(APIView):
    def get(self, requset, quiz_id=None):
        pass

    def post(self, request, quiz_id=None):
        # 복습노트에 저장
        if quiz_id:
            select = request.data.get("select")
            user = request.user
            quiz = get_object_or_404(ReadingQuiz, pk=quiz_id)
            if quiz not in user.reading_quizzes.all():
                user.reading_quizzes.add(quiz, through_defaults={"select": select})
                return Response({"detail": "저장 완료"}, status=status.HTTP_200_OK)
            return Response({"detail": "이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 문장 생성
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": content},
                ],
                temperature=2,
                finish_reason="length",
                # stream=True,
            )
            response = json.loads(response)
            data = response["choices"][0]["message"]["content"]
            serializer = ReadingQuizSerializer(data=data)
            level = Level.objects.get(name="C1")
            if serializer.is_valid():
                serializer.save(level=level)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "생성 실패"}, status=status.HTTP_400_BAD_REQUEST)

    # 복습노트에서 제거
    def delete(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(ReadingQuiz, pk=quiz_id)
        if quiz in user.reading_quizzes.all():
            user.reading_quizzes.remove(quiz)
            return Response({"detail": "제거 완료"}, status=status.HTTP_200_OK)
        return Response({"detail": "이미 제거되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


class WordView(APIView):
    CORRECT_WORDS_COUNT = 10
    WRONG_WORDS_PER_QUIZ = 3

    # 단어 퀴즈 보기
    def get(self, request):
        try:
            # Word 전체 리스트를 랜덤하게 정렬한 뒤 40개 가져오기
            all_words = list(Word.objects.order_by("?")[: self.CORRECT_WORDS_COUNT * 4])
            correct_words = all_words[: self.CORRECT_WORDS_COUNT]
            remain_words = all_words[self.CORRECT_WORDS_COUNT :]

            quizzes = []
            for index in range(self.CORRECT_WORDS_COUNT):
                # 0번째 단어
                # 1번째 단어
                # 2번째 단어
                correct_word = correct_words[index]

                # 0~2번째 틀린 단어
                # 3~5번째 틀린 단어
                # 6~8번째 틀린 단어
                wrong_words = remain_words[
                    index
                    * self.WRONG_WORDS_PER_QUIZ : (index + 1)
                    * self.WRONG_WORDS_PER_QUIZ
                ]

                quiz = {
                    "word": correct_word.content,
                    "meaning": correct_word.meaning,
                    "wrong": [word.meaning for word in wrong_words],
                }
                quizzes.append(quiz)

            # serializer = WordQuizesSerializer(quizes, many=True)
            return Response(quizzes, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # DB 단어장에 단어 추가
    def post(self, request):
        content = request.data["word"]
        words = Word.objects.all()
        if content not in words:
            meaning = GoogleTranslator(source="en", target="ko").translate(text=content)
            new_word = Word(content=content, meaning=meaning)
            new_word.save()
            serializer = WordSerializer(new_word)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "단어가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)


class WordsBookView(APIView):
    # 내 단어장 보기
    def get(self, request):
        user = request.user
        words = user.words
        if words.exists():
            serializer = MyWordSerializer(words, many=True)
            serialized_words = serializer.data

            # response_data = {"vocabulary": [{"word":word["content"], "meaning":word["meaning"]} for word in serialized_words]}
            response_data = {"vocabulary": serialized_words}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"No words associated with this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # 내 단어장에 단어 추가
    def post(self, request, word_id):
        user = request.user
        words = user.words
        word = get_object_or_404(Word, pk=word_id)
        if word not in words:
            words.add(word)
            return Response(
                {"detail": "내 단어장에 단어가 추가되었습니다."}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "내 단어장에 단어가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    # 내 단어장의 단어 삭제
    def delete(self, request, word_id):
        user = request.user
        words = user.words  # 유저의 단어장에 있는 모든 단어
        word = get_object_or_404(Word, pk=word_id)
        if word in words:
            words.remove(word)
            return Response({"detail": "삭제되었습니다."}, status=status.HTTP_200_OK)
        return Response({"detail": "단어가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# class DialogueView(APIView):
#     def post(self, request):
#         scenario_id = request.data["scenarioId"]
#         scenario = get_object_or_404(Scenario, scenario_id)
#         content = f"""
#             Write a single dialogue between a(an) {scenario.you} and {scenario.me} who {scenario.action}.
#             You are a(an) {scenario.you} and I am a(an) {scenario.me}.
#             Please write a short one dialogue containing 5 conversations.
#             Please write a dialogue using A2 level words.
#         """
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             provider=openai.Provider.GptGo,
#             messages=[
#                 {"role": "system", "content": content},
#             ],
#             stream=True,
#         )
#         for message in response:
#             print(message)
