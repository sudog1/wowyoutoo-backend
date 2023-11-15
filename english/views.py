from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ReadingProblem
from rest_framework import status
from .constants import content
import g4f as openai
import json

from g4f.Provider import (
    AiAsk,
    ChatgptAi,
    GptGo,
    FreeGpt,
)


# Create your views here.
class PassageCreateView(APIView):
    def post(self, request):
        pass


class ReadingView(APIView):
    def get(self, requset, problem_id=None):
        pass

    def post(self, request, problem_id=None):
        # 복습노트에 저장
        if problem_id:
            user = request.user
            problem = get_object_or_404(ReadingProblem, pk=problem_id)
            problems = user.reading_problems
            if problem not in problems:
                problems.add(problem)
                return Response({"detail": "저장 완료"}, status=status.HTTP_200_OK)
            return Response({"detail": "이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 단어 생성
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

    def delete(self, request, problem_id=None):
        pass


class WordView(APIView):
    def get(self, requset):
        pass

    def post(self, request):
        pass


class WordsBookView(APIView):
    def get(self, request, user_id):
        pass

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
