from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config.settings import AUTH_USER_MODEL


# Create your models here.
class Payment(models.Model):
    merchant_uid = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(100, message="100원 부터 결제가 가능합니다.")])
    paid_amount = models.PositiveIntegerField(blank=True, null=True)
    
    
class Product(models.Model):
    pass