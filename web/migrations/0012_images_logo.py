# Generated by Django 3.2.7 on 2021-10-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0011_alter_images_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="images",
            name="logo",
            field=models.BooleanField(
                default=False, verbose_name="Logo główne"
            ),
        ),
    ]
