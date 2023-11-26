from rest_framework import serializers
from .models import Payment


class PrepareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "merchant_uid",
            "amount",
        )
