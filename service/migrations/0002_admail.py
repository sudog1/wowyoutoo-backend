# Generated by Django 4.2.7 on 2023-11-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0001_initial"),
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
    ]
