# Generated by Django 3.2.7 on 2022-03-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20220317_0747'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vat',
            options={'ordering': ('name',), 'verbose_name_plural': 'Podatek Vat'},
        ),
        migrations.AddField(
            model_name='products',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla produktu'),
        ),
        migrations.AddField(
            model_name='products',
            name='meta_title',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla produktu'),
        ),
    ]
