from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.generics import get_object_or_404
from config.settings import AUTH_USER_MODEL
from .serializers import AnnoucementListSerializer,AnnoncementSerializer,QnaListSerializer,QnaSerializer,QnaResponseSerializer
from .models import Announcement,Qna,QnaResponse
from .permissions import ReadOnlyPermission
from .pagenation import PostPageNumberPagination
# Create your views here.
class AnnouncementView(APIView):
    permission_classes=[ReadOnlyPermission]
    def get(self,request,announcement_id=None):
        if announcement_id==None:
            announcements=Announcement.objects.all().order_by("-created_at")
            serializer=AnnoucementListSerializer(announcements,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            announcement=get_object_or_404(Announcement,pk=announcement_id)
            serializer=AnnoncementSerializer(announcement)
            return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=AnnoncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,announcement_id):
        announcement=get_object_or_404(Announcement,pk=announcement_id)
        serializer=AnnoncementSerializer(announcement,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,announcement_id):
        announcement=get_object_or_404(Announcement,pk=announcement_id)
        announcement.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)
    
class QnaView(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    def get(self,request,qna_id=None,format=None):
        if qna_id==None:
            qnas=Qna.objects.select_related("author").all().order_by("-created_at")
            pagenator = self.pagination_class()
            page = pagenator.paginate_queryset(qnas, request)
            serializer=pagenator.get_paginated_response(QnaListSerializer(page,many=True).data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            qna=get_object_or_404(Qna.objects.select_related("author"),pk=qna_id)
            if qna.is_private==True:
                return Response({"message":"권한이없습니다"},status=status.HTTP_403_FORBIDDEN)
            serializer=QnaSerializer(qna)
            return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=QnaSerializer(data=request.data)
        if serializer.is_valid():
            user=request.user
            serializer.save(author=user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,qna_id):
        qna=get_object_or_404(Qna,pk=qna_id)
        serializer=QnaSerializer(qna,data=request.data,partial=True)
        if request.user!=qna.author:
            return Response({"message":"권한이없습니다"},status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,qna_id):
        qna=get_object_or_404(Announcement,pk=qna_id)
        if request.user!=qna.author:
            return Response({"message":"권한이없습니다"},status=status.HTTP_403_FORBIDDEN)
        qna.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)
class QnaResponseView(APIView):
    permission_classes=[ReadOnlyPermission]
    def get(self,request,qna_id):
        qna=get_object_or_404(Qna.objects.select_related("author"),pk=qna_id)
        if qna.is_private==True:
            return Response({"message":"권한이없습니다"},status=status.HTTP_403_FORBIDDEN)
        qna_response=get_object_or_404(QnaResponse,pk=qna_id)
        serializer=QnaResponseSerializer(qna_response)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,qna_id):
        qna=get_object_or_404(Qna,pk=qna_id)
        serializer=QnaResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(qna=qna)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,reques,qna_id):
        qna_response=get_object_or_404(QnaResponse,pk=qna_id)
        qna_response.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)
    def put(self,request,qna_id):
        qna_response=get_object_or_404(QnaResponse,pk=qna_id)
        serializer=QnaResponseSerializer(qna_response,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(qna=qna_id)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)