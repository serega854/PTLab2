# Generated by Django 5.1.4 on 2024-12-21 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="total_price",
            field=models.PositiveIntegerField(default=0),
        ),
    ]