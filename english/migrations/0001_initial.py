# Generated by Django 4.2.7 on 2023-11-27 15:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Level",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("step", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="ReadingQuiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("paragraph", models.TextField()),
                ("question", models.CharField(max_length=255)),
                ("answers", models.JSONField()),
                (
                    "solution",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                ("explanation", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reading_quizzes",
                        to="english.level",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Word",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("term", models.CharField(max_length=30)),
                ("meaning", models.CharField(max_length=30)),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="words", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Select",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "index",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(3),
                            django.core.validators.MinValueValidator(0),
                        ]
                    ),
                ),
                (
                    "reading_quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="selects",
                        to="english.readingquiz",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="selects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="readingquiz",
            name="users",
            field=models.ManyToManyField(
                related_name="reading_quizzes",
                through="english.Select",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
