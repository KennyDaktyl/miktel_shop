# Generated by Django 3.2.7 on 2022-02-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0031_auto_20220213_1135"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="prodcuts_item",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Produkty"
            ),
        ),
    ]
