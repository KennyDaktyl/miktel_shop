# Generated by Django 3.2.7 on 2021-10-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_images_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='description',
            field=models.TextField(blank=True, max_length=264, null=True, verbose_name='Mały opis dla obrazka na karuzeli'),
        ),
    ]