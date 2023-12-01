# Generated by Django 4.2.7 on 2023-12-01 01:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("service", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qna",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="qnas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="qna",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/service/qna"
            ),
        ),
        migrations.AlterField(
            model_name="qnaresponse",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/service/qna"
            ),
        ),
    ]
