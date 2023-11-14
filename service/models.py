from django.db import models
from config.settings import AUTH_USER_MODEL
# Create your models here

class Announcement(models.Model):
    title=models.CharField(max_length=64)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(
        upload_to="media/service/announcement",
        blank=True,
        null=True,
    )
class Qna(models.Model):
    QUESTION_CHOICE = (
        ("study", "study"),
        ("userinfo", "userinfo"),
        ("error","error"),
        ("point","point"),
        ("etc", "etc"),
    )
    author=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='faqs')
    title=models.CharField(max_length=64)
    content=models.TextField()
    is_private=models.BooleanField(default=False)
    is_answered=models.BooleanField(default=False)
    question_type=models.CharField(max_length=10, choices=QUESTION_CHOICE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(
        upload_to="media/service/faq",
        blank=True,
        null=True,
    )

class QnaResponse(models.Model):
    qna=models.OneToOneField(to=Qna,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(
        upload_to="media/service/faq",
        blank=True,
        null=True,
    )