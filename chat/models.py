from django.db import models
from config.settings import AUTH_USER_MODEL
from english.models import Level


# Create your models here.
class AIChatLog(models.Model):
    messages = models.JSONField()
    scenario = models.TextField()
    # token_count = models.PositiveIntegerField(default=0)
    ongoing = models.BooleanField(default=False)
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_chatlog"
    )
