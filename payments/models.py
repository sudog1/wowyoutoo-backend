from django.db import models
from django.core.validators import MinValueValidator
from config.settings import AUTH_USER_MODEL


# Create your models here.       
class Product(models.Model):
    
    class Status(models.TextChoices):
        ACTIVE = "active", "정상"
        SOLD_OUT = "sold_out", "품절"
        INACTIVE = "inactive", "비활성화"
    
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.PositiveIntegerField(validators=[MinValueValidator(100, message="100원 이상")])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Payment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_payment_set")
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    merchant_uid = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(100, message="100원 부터 결제가 가능합니다.")])
    paid_amount = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_cart_set")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cart_set")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1, message="1개 이상")])
    

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_order_set")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
