from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from english.models import ReadingPassage
from english.serializers import PassageListSerializer, PassageDetailSerializer


# Create your views here.
class PassageCreateView(APIView):
    def post(self, request):
        pass


class PassageView(APIView):
    def get(self, requset, passage_id=None):
        if passage_id:
            #상세보기
            passage = get_object_or_404(ReadingPassage, pk=passage_id)
            serializer = PassageDetailSerializer(passage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            #전체보기
            passages = ReadingPassage.objects.all()
            serializer = PassageListSerializer(passages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
