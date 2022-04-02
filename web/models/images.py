import sys
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_resized import ResizedImageField
from PIL import Image

from .base import BaseModel

def file_size(value):
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("Plik który chcesz wrzucić jest większy niż 6MB.")


class Images(BaseModel):
    id = models.AutoField(primary_key=True)
    image =  ResizedImageField(
        verbose_name="Zdjęcie główne",
        size=[800, 600],
        upload_to="images/gallery/",
        validators=[file_size],
        null=True,
        blank=True,
    )
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(
        verbose_name="Title dla obrazka", blank=True, null=True, max_length=70
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Zdjęcia kategorii",
        related_name="category_gallery",
    )
    product = models.ForeignKey(
        "Products",
        db_index=True,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Zdjęcie na galerie",
        related_name="product_gallery",
    )
    article = models.ForeignKey(
        "Articles",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Zdjęcie dla artykułu",
        related_name="articles_gallery",
    )
    main = models.BooleanField(verbose_name="Zdjęcie główne", default=False)
    stamp = models.BooleanField(verbose_name="Zdjęcie wzornika?", default=False)
    carousel = models.BooleanField(verbose_name="Zdjęcie na karuzele?", default=False)
    description = models.TextField(
        verbose_name="Mały opis dla obrazka na karuzeli",
        blank=True,
        null=True,
        max_length=264,
    )
    logo = models.BooleanField(verbose_name="Logo główne", default=False)

    class Meta:
        ordering = (
            "-id",
            "image",
        )
        verbose_name_plural = "Galeria"

    def save(self):
        im = Image.open(self.image)
        output = BytesIO()
        im.save(output, format="WEBP", quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.webp" % self.image.name.split(".")[0],
            "image/webp",
            sys.getsizeof(output),
            None,
        )
        super(Images, self).save()

    def __str__(self):
        return str(self.image)
