# Generated by Django 3.2.7 on 2022-03-15 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='meta_description',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Meta description dla kategorii'),
        ),
    ]
