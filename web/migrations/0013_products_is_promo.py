# Generated by Django 3.2.7 on 2021-10-01 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_images_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_promo',
            field=models.BooleanField(default=False, verbose_name='Czy jest w propozycjach'),
        ),
    ]
