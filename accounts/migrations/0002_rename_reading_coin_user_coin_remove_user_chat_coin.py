# Generated by Django 4.2.7 on 2023-11-29 11:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="reading_coin",
            new_name="coin",
        ),
        migrations.RemoveField(
            model_name="user",
            name="chat_coin",
        ),
    ]