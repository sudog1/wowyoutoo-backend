from rest_framework import serializers
from .models import Payment, Product


class PrepareSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    
    class Meta:
        model = Payment
        fields = (
            "id",
            "merchant_uid",
            "amount",
            "product_name",
            "email",
        )
        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "description",
            "price",
            "status",
        )