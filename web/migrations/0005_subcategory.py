# Generated by Django 3.2.7 on 2021-09-22 06:51

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import web.models.products


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_remove_productcopy_color_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa podkategorii')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Numer kategorii')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[1280, 960], upload_to='images/categorys/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category', verbose_name='Kategoria podkategorii')),
            ],
            options={
                'verbose_name_plural': 'PodKategorie produktów',
                'ordering': ('number', 'name'),
            },
        ),
    ]
