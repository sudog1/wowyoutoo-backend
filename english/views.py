from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class PassageCreateView(APIView):
    def post(self, request):
        pass


class PassageView(APIView):
    def get(self, requset, passage_id=None):
        return Response("yasgtest")

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
