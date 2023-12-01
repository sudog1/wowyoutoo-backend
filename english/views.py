from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from django.shortcuts import get_object_or_404
from .models import ReadingQuiz, Select
from rest_framework import status
from .constants import (
    CONTENT,
    READING_COST,
    READING_QUIZ_COUNT,
    CORRECT_WORDS_COUNT,
    WRONG_WORDS_PER_QUIZ,
)
import json
from django.db.models import F
from .models import Word, ReadingQuiz, Select
from .serializers import (
    MyWordSerializer,
    ReadingQuizListSerializer,
    WordQuizesSerializer,
    WordSerializer,
    ReadingQuizSerializer,
)
from deep_translator import (
    GoogleTranslator,
    DeeplTranslator,
)
from django.db import IntegrityError
import random

from openai import AsyncOpenAI
from config.settings import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# 지문 생성
class CreateReadingView(APIView):
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        user = request.user
        if user.coin >= READING_COST:
            user.coin -= READING_COST
            await user.asave()
        else:
            return Response(
                {"detail": "결제 필요"}, status=status.HTTP_402_PAYMENT_REQUIRED
            )
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CONTENT},
            ],
            seed=random.randrange(2147483647),
            temperature=1,
        )
        data = json.loads(response.choices[0].message.content)
        try:
            quiz = await ReadingQuiz.objects.acreate(**data)
            serializer = ReadingQuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"detail": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # serializer = ReadingQuizSerializer(data=data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ReadingView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 기존 독해문제 리스트
    def get(self, request):
        try:
            quizzes = list(ReadingQuiz.objects.order_by("?")[:READING_QUIZ_COUNT])
            serializer = ReadingQuizSerializer(quizzes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # 푼 독해문제 카운트
    def post(self, request):
        user = request.user
        user.reading_nums += 1
        user.save()
        return Response(status=status.HTTP_200_OK)


# 유저의 복습노트 관련 뷰
class ReadingBookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id=None):
        # 복습할 독해문제 상세보기
        if quiz_id:
            quiz = get_object_or_404(ReadingQuiz, pk=quiz_id)
            user = request.user
            select = get_object_or_404(Select, user=user, reading_quiz=quiz)
            serializer = ReadingQuizSerializer(quiz)
            data = serializer.data
            data["select"] = select.index
            return Response(data, status=status.HTTP_200_OK)
        # 복습노트의 독해문제 리스트
        else:
            user = request.user
            quizzes = user.reading_quizzes.all()
            serializer = ReadingQuizListSerializer(quizzes, many=True)
            try:
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(
                    serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def post(self, request, quiz_id):
        # 복습노트에 저장
        select = request.data.get("select")

        user = request.user
        quiz = get_object_or_404(ReadingQuiz, pk=quiz_id)

        if quiz not in user.reading_quizzes.all():
            user.reading_quizzes.add(quiz, through_defaults={"index": select})
            return Response({"detail": "저장 완료"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 복습노트에서 제거
    def delete(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(ReadingQuiz, pk=quiz_id)
        if quiz in user.reading_quizzes.all():
            user.reading_quizzes.remove(quiz)
            return Response({"message": "제거 완료"}, status=status.HTTP_200_OK)
        return Response({"message": "이미 제거되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


class WordView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 단어 퀴즈 보기
    def get(self, request):
        try:
            # Word 전체 리스트를 랜덤하게 정렬한 뒤 40개 가져오기
            words_count = request.data.get("words_count", CORRECT_WORDS_COUNT)
            all_words = list(Word.objects.order_by("?")[: words_count * 4])
            correct_words = all_words[:words_count]
            remain_words = all_words[words_count:]

            quizzes = []
            for index in range(words_count):
                # 0번째 단어
                correct_word = correct_words[index]

                # 0~2번째 틀린단어
                wrong_words = remain_words[
                    index * WRONG_WORDS_PER_QUIZ : (index + 1) * WRONG_WORDS_PER_QUIZ
                ]

                quiz = {
                    "id": correct_word.id,
                    "term": correct_word.term,
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

    # DB에 단어 추가
    def post(self, request, word_id=None):
        # 푼 단어 카운트
        if word_id:
            user = request.user
            user.word_nums += 1
            user.save()
            return Response(status=status.HTTP_200_OK)
        term = request.data["term"]
        try:
            word = Word.object.get(term=term)
            serializer = WordSerializer(word)
            return Response(serializer.data, status=status.HTTP_200_BAD_REQUEST)
        except Exception as e:
            meaning = GoogleTranslator(source="en", target="ko").translate(text=term)
            serializer = WordSerializer(term=term, meaning=meaning)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class WordsBookView(APIView):
    permission_classes = [IsAuthenticated]

    # 내 단어장 보기
    def get(self, request):
        user = request.user
        words = user.words.all()
        if words.exists():
            serializer = WordSerializer(words, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "저장된 단어가 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # 내 단어장에 단어 추가
    def post(self, request, word_id):
        user = request.user
        words = user.words.all()
        word = get_object_or_404(Word, pk=word_id)
        if word not in words:
            user.words.add(word)
            return Response(
                {"message": "내 단어장에 단어가 추가되었습니다."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "내 단어장에 단어가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    # 내 단어장에서 단어 제거
    def delete(self, request, word_id):
        user = request.user
        words = user.words.all()  # 유저의 단어장에 있는 모든 단어
        word = get_object_or_404(Word, pk=word_id)
        if word in words:
            words.remove(word)
            return Response({"message": "제거되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "단어가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
