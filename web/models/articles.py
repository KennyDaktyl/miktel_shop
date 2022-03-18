from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_resized import ResizedImageField

from .base import BaseModel
from .images import Images

def file_size(value):
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("Plik który chcesz wrzucić jest większy niż 6MB.")


class Articles(BaseModel):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        "category", on_delete=models.CASCADE, verbose_name="Kategoria artykułu"
    )
    title = models.CharField(verbose_name="Tytyuł artykułu", max_length=256)
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True, max_length=256)
    body = models.TextField(verbose_name="Treść artukułu")
    image = ResizedImageField(
        verbose_name="Zdjęcie główne",
        size=[1280, 960],
        upload_to="images/articles/",
        validators=[file_size],
        null=True,
        blank=True,
    )
    image_alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    image_title = models.CharField(
        verbose_name="Title dla obrazka", blank=True, null=True, max_length=70
    )
    meta_description = models.CharField(
        verbose_name="Meta description dla artykułu", blank=True, null=True, max_length=160
    )
    meta_title = models.CharField(
        verbose_name="Meta title dla artykułu", blank=True, null=True, max_length=60
    )
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Articles, self).save()

    def get_absolute_url(self):
        return reverse(
            "article_details",
            kwargs={
                "category": self.category.slug,
                "title": self.slug,
                "pk": self.id,
            },
        )

    class Meta:
        ordering = ("-created_time",)
        verbose_name_plural = "Artykuły"
    
    def images(self):
        return Images.objects.filter(article_id=self)

    def __str__(self):
        return self.category.name + ", " + self.title
