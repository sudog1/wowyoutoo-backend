# Generated by Django 4.2.7 on 2023-11-29 23:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("english", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="readingquiz",
            old_name="answers",
            new_name="options",
        ),
    ]