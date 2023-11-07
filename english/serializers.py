from rest_framework import serializers
from english.models import ReadingPassage


class PassageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingPassage
        fields = ("title", "created_at", "difficult")
        

class PassageDetailSerializer(serializers.ModelSerializer):
    wrong = serializers.SerializerMethodField()
    def get_wrong(self, obj):
        return list(obj.wrong.split(","))
    
    difficult = serializers.SerializerMethodField()
    def get_difficult(self, obj):
        return obj.difficult.step
    
    class Meta:
        model = ReadingPassage
        fields = ("title", "content", "correct", "wrong", "created_at", "difficult")
    