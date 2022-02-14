# Generated by Django 3.2.7 on 2022-01-31 17:09

import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
from django.db import migrations, models

import web.models.articles


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0028_merge_20220120_1822"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="name",
            field=models.CharField(
                db_index=True, max_length=128, verbose_name="Nazwa produktu"
            ),
        ),
        migrations.CreateModel(
            name="Articles",
            fields=[
                (
                    "created_time",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "modified_time",
                    models.DateTimeField(auto_now=True, db_index=True),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(
                        max_length=256, verbose_name="Tytyuł artykułu"
                    ),
                ),
                ("body", models.TextField(verbose_name="Treść artukułu")),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        null=True,
                        quality=100,
                        size=[1280, 960],
                        upload_to="images/articles/",
                        validators=[web.models.articles.file_size],
                        verbose_name="Zdjęcie główne",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.category",
                        verbose_name="Kategoria artykułu",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Artykuły",
                "ordering": ("-created_time",),
            },
        ),
    ]
