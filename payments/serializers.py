from rest_framework import serializers
from .models import Payment, Product, CartItem


class PrepareSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "merchant_uid",
            "amount",
            "product_name",
            # "email",
        )
        
        # extra_kwargs = {"user":{"allow_null":True}}
        


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
    

class NestedListSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()

# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = (
#             "product_id",
#             ""
#         )