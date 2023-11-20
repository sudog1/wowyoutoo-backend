from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ReadingQuiz
from rest_framework import status
from .constants import content
import g4f as openai
import json
from .models import Word, ReadingQuiz, Level
from .serializers import WordQuizesSerializer, WordSerializer, ReadingQuizSerializer


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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=openai.Provider.GptGo,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": content},
                ],
                temperature=2,
                finish_reason="length",
                # stream=True,
            )
            response = json.loads(response)
            serializer = ReadingQuizSerializer(data=response)
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
    def get(self, requset):
        quizes = []
        # Word 전체 리스트를 랜덤하게 정렬한 뒤 40개 가져오기
        all_words = list(Word.objects.order_by("?")[:40])
        correct_words = all_words[:10]
        remain_words = all_words[10:]
        for i in range(10):
            # 0번째 단어
            # 1번째 단어
            # 2번째 단어
            correct_word = correct_words[i]
            # 0~2번째 틀린 단어
            # 3~5번째 틀린 단어
            # 6~8번째 틀린 단어
            wrong_words = remain_words[i * 3 : (i + 1) * 3]

            quize = {
                "word": correct_word.content,
                "meaning": correct_word.meaning,
                "wrong": [word.meaning for word in wrong_words],
            }
            quizes.append(quize)
        # serializer = WordQuizesSerializer(quizes, many=True)
        return Response(quizes, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class WordsBookView(APIView):
    def get(self, request, user_id):
        words = Word.objects.filter(user__pk=user_id)
        if words.exists():
            serializer = WordSerializer(words, many=True)
            serialized_words = serializer.data

            # response_data = {"vocabulary": [{"word":word["content"], "meaning":word["meaning"]} for word in serialized_words]}
            response_data = {"vocabulary": serialized_words}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"No words associated with this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, word_id):
        pass

    def delete(self, request, user_id, word_id):
        pass


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
