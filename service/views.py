from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from config.settings import AUTH_USER_MODEL
from .serializers import (
    AnnoucementListSerializer,
    AnnoncementSerializer,
    QnaListSerializer,
    QnaSerializer,
    QnaCreateSerializer,
    QnaResponseSerializer,
    AdMailSerializer,
)
from .models import Announcement, Qna, QnaResponse
from .permissions import ReadOnlyPermission
from .pagenation import PostPageNumberPagination
from .tasks import send_email
from celery import group
from accounts.models import User


# Create your views here.
class AnnouncementView(APIView):
    permission_classes = [ReadOnlyPermission] 

    def get(self, request, announcement_id=None):
        if announcement_id == None:
            announcements = Announcement.objects.all().order_by("-created_at")
            serializer = AnnoucementListSerializer(announcements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            announcement = get_object_or_404(Announcement, pk=announcement_id)
            serializer = AnnoncementSerializer(announcement)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_admin!=True:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        serializer = AnnoncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, announcement_id):
        if request.user.is_admin!=True:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        serializer = AnnoncementSerializer(
            announcement, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, announcement_id):
        if request.user.is_admin!=True:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        announcement.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)


class QnaView(APIView):
    pagination_class = PostPageNumberPagination
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, qna_id=None, format=None):
        if qna_id == None:
            qnas = Qna.objects.select_related("author").all().order_by("-created_at")
            pagenator = (
                self.pagination_class()
            )  # pagenation.py에서 커스터마이징한 페이지네이터 클래스로 인스턴스생성
            page = pagenator.paginate_queryset(
                qnas, request
            )  # page의 타입은 리스트입니다,page_size = 15 만큼 원소를 가지며,원소는 qna입니다
            serializer = pagenator.get_paginated_response(
                QnaListSerializer(page, many=True).data
            )  # 제이슨형식으로 반환할 데이터
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            qna = get_object_or_404(Qna.objects.select_related("author"), pk=qna_id)
            if hasattr(request.user, "is_admin"):
                pass
            elif qna.is_private == True and request.user!=qna.author:
                return Response(
                    {"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN
                )
            serializer = QnaSerializer(qna)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QnaCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, qna_id):
        qna = get_object_or_404(Qna, pk=qna_id)
        serializer = QnaCreateSerializer(qna, data=request.data, partial=True)
        if request.user != qna.author:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, qna_id):
        qna = get_object_or_404(Qna, pk=qna_id)
        if request.user != qna.author:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        qna.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)


class QnaResponseView(APIView):
    permission_classes = [ReadOnlyPermission] 
    def get(self, request, qna_id):
        qna = get_object_or_404(Qna.objects.select_related("author"), pk=qna_id)
        if qna.is_private == True and request.user!=qna.author:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        qna_response = get_object_or_404(QnaResponse, qna_id=qna_id)
        serializer = QnaResponseSerializer(qna_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, qna_id):
        if request.user.is_admin!=True:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        qna=Qna.objects.get(pk=qna_id)
        serializer = QnaResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(qna=qna)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, qna_id):
        if request.user.is_admin!=True:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        qna_response = get_object_or_404(QnaResponse, qna_id=qna_id)
        qna_response.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)

    def put(self, request, qna_id):
        if request.user.is_admin!=True:
            return Response({"message": "권한이없습니다"}, status=status.HTTP_403_FORBIDDEN)
        qna_response = get_object_or_404(QnaResponse, qna_id=qna_id)
        serializer = QnaResponseSerializer(
            qna_response, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BackOfficeView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({"detail": "인증되었습니다"}, status=status.HTTP_200_OK)

    def post(self, request):
        email_list = list(
            User.objects.filter(verified=True)
            .values_list("email", flat=True)
        )  # flat을 사용하지않으면 리스트에 튜플이 담겨나옵니다
        serializer = AdMailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        result = send_email.s(email_list, serializer.data).delay()
        return Response(result.id)
