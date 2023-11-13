from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config.settings import AUTH_USER_MODEL


# Create your models here.
class Difficulty(models.Model):
    level = models.SmallIntegerField(
        primary_key=True, validators=[MaxValueValidator(6), MinValueValidator(1)]
    )
    name = models.CharField(max_length=30)


class ReadingPassage(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    correct = models.CharField(max_length=50)
    wrong = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    difficult = models.ForeignKey(
        Difficulty, on_delete=models.CASCADE, related_name="passages"
    )


class Select(models.Model):
    select = models.SmallIntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selects"
    )
    passage = models.OneToOneField(ReadingPassage, on_delete=models.CASCADE)


class Word(models.Model):
    content = models.CharField(max_length=30)
    meaning = models.CharField(max_length=30)
    user = models.ManyToManyField(AUTH_USER_MODEL, related_name="words")


class Scenario(models.Model):
    location = models.CharField(max_length=30)
    you = models.CharField(max_length=30)
    me = models.CharField(max_length=30)
    action = models.TextField()
