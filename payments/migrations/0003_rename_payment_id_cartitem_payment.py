# Generated by Django 4.2.7 on 2023-11-29 08:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0002_cartitem_payment_id_alter_cartitem_user_orderitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="payment_id",
            new_name="payment",
        ),
    ]
