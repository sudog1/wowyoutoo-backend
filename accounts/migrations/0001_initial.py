# Generated by Django 4.2.7 on 2023-11-06 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=30, unique=True, verbose_name="아이디"),
                ),
                ("password", models.CharField(max_length=255, verbose_name="비밀번호")),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "profile_img",
                    models.ImageField(
                        blank=True,
                        default="media/userProfile/default.png",
                        null=True,
                        upload_to="media/userProfile",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False, verbose_name="관리자 여부")),
                ("updated_at", models.DateField(auto_now=True, verbose_name="수정일")),
                ("verified", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
