# Generated by Django 5.1.4 on 2024-12-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_remove_purchase_date_remove_purchase_total_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="quantity_beg",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
