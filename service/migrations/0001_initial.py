# Generated by Django 4.2.7 on 2023-11-27 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AdMail",
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
                ("title", models.CharField(max_length=60)),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/service/ad_mail"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Announcement",
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
                ("title", models.CharField(max_length=64)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/service/announcement"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Qna",
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
                ("title", models.CharField(max_length=64)),
                ("content", models.TextField()),
                ("is_private", models.BooleanField(default=False)),
                ("is_answered", models.BooleanField(default=False)),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("study", "study"),
                            ("userinfo", "userinfo"),
                            ("error", "error"),
                            ("point", "point"),
                            ("etc", "etc"),
                        ],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/service/faq"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="faqs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QnaResponse",
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
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/service/faq"
                    ),
                ),
                (
                    "qna",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="service.qna"
                    ),
                ),
            ],
        ),
    ]
