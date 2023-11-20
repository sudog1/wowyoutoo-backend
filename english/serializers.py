from rest_framework import serializers
from .models import Word, ReadingQuiz


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = (
            "content",
            "meaning",
        )


class MyWordSerializer(serializers.ModelSerializer):
    word = serializers.CharField(source="content")

    class Meta:
        model = Word
        fields = (
            "word",
            "meaning",
        )


class WordQuizesSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=20)
    meaning = serializers.CharField(max_length=20)
    wrong = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = Word
        fields = (
            "word",
            "meaning",
            "wrong",
        )


class ReadingQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingQuiz
        fields = (
            "title",
            "paragraph",
            "answers",
            "solution",
            "explanation",
        )
