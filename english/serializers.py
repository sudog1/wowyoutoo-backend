from rest_framework import serializers
from .models import Word, ReadingQuiz


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = (
            "id",
            "term",
            "meaning",
        )


class MyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = (
            "term",
            "meaning",
        )


class WordQuizesSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=20)
    meaning = serializers.CharField(max_length=20)
    wrong = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = Word
        fields = (
            "term",
            "meaning",
            "wrong",
        )


class ReadingQuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingQuiz
        fields = (
            "id",
            "title",
            "paragraph",
        )


class ReadingQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingQuiz
        fields = (
            "id",
            "title",
            "paragraph",
            "question",
            "options",
            "solution",
            "explanation",
        )
