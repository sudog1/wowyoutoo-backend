from .models import Qna,QnaResponse,Announcement
from rest_framework import serializers
class AnnoncementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields='__all__'

class AnnoucementListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields=["title","created_at",'updated_at']

class QnaListSerializer(serializers.ModelSerializer):
    author=serializers.SerializerMethodField()
    def get_author(self,obj):
        return {obj.author.username,obj.author.id}
    class Meta:
        model=Qna
        fields=["title","author","created_at","is_answered"]

class QnaSerializer(serializers.ModelSerializer):
    author=serializers.SerializerMethodField()
    def get_author(self,obj):
        return {obj.author.username,obj.author.id}
    class Meta: 
        model=Qna
        fields='__all__'

class QnaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=QnaResponse
        fields=["content","created_at","updated_at","image"]