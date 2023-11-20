from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config.settings import AUTH_USER_MODEL


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=10)


class ReadingQuiz(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.TextField()
    answers = models.JSONField()
    solution = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ]
    )
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(
        Level, on_delete=models.PROTECT, related_name="reading_quizzes"
    )
    users = models.ManyToManyField(
        AUTH_USER_MODEL,
        through="Select",
        related_name="reading_quizzes",
    )


class Select(models.Model):
    select = models.SmallIntegerField(
        validators=[MaxValueValidator(3), MinValueValidator(0)]
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selects"
    )
    reading_quiz = models.ForeignKey(
        ReadingQuiz, on_delete=models.CASCADE, related_name="selects"
    )


class Word(models.Model):
    content = models.CharField(max_length=30)
    meaning = models.CharField(max_length=30)
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name="words")


# class Scenario(models.Model):
#     location = models.CharField(max_length=30)
#     you = models.CharField(max_length=30)
#     me = models.CharField(max_length=30)
#     action = models.TextField()
