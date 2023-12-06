from .models import Qna, QnaResponse, Announcement, AdMail
from rest_framework import serializers


class AnnoncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"


class AnnoucementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "title", "created_at", "updated_at"]


class QnaListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"nickname": obj.author.nickname, "id": obj.author.id}

    class Meta:
        model = Qna
        fields = [
            "id",
            "title",
            "author",
            "created_at",
            "is_answered",
            "is_private",
            "question_type",
        ]


class QnaSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"nickname": obj.author.nickname, "id": obj.author.id}

    class Meta:
        model = Qna
        fields = "__all__"


class QnaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ["title", "content", "image", "is_private", "question_type"]


class QnaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaResponse
        fields = ["content", "created_at", "updated_at", "image"]


class AdMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdMail
        fields = "__all__"
