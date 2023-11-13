from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Scenario
import g4f as openai

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


class PassageView(APIView):
    def get(self, requset, passage_id=None):
        pass

    def post(self, request):
        pass

    def delete(self, request, passage_id):
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


class DialogueView(APIView):
    def post(self, request):
        scenario_id = request.data["scenarioId"]
        scenario = get_object_or_404(Scenario, scenario_id)
        content = f"""
            Write a single dialogue between a(an) {scenario.you} and {scenario.me} who {scenario.action}.
            You are a(an) {scenario.you} and I am a(an) {scenario.me}.
            Please write a short one dialogue containing 5 conversations.
            Please write a dialogue using A2 level words.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=openai.Provider.GptGo,
            messages=[
                {"role": "system", "content": content},
            ],
            stream=True,
        )
        for message in response:
            print(message)
