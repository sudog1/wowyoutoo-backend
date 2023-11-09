from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config.settings import AUTH_USER_MODEL


# Create your models here.
class ReadingPassage(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    correct = models.CharField(max_length=50)
    wrong = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    difficult = models.ForeignKey(
        "Difficult", on_delete=models.CASCADE, related_name="passages"
    )


class Select(models.Model):
    select = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selects"
    )
    passage = models.OneToOneField(ReadingPassage, on_delete=models.CASCADE)


class Difficult(models.Model):
    step = models.IntegerField(validators=MinValueValidator(1))


class Word(models.Model):
    content = models.CharField(max_length=30)
    meaning = models.CharField(max_length=30)
    user = models.ManyToManyField(AUTH_USER_MODEL, related_name="words")
