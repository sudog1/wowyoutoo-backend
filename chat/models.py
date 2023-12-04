from django.db import models
from config.settings import AUTH_USER_MODEL


# Create your models here.
class AIChatLog(models.Model):
    messages = models.JSONField(default=list)
    ongoing = models.BooleanField(default=False)
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_chatlog"
    )
