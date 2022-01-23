from typing import cast
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from django_resized import ResizedImageField
from django.core.exceptions import ValidationError
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from decimal import Decimal

from .base import BaseModel


def file_size(value):
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            'Plik który chcesz wrzucić jest większy niż 6MB.')


class Store(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa magazynu", max_length=64)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              null=True,
                              blank=True,
                              upload_to='images/workplace/',
                              validators=[file_size])
    phone_number = models.CharField(
        verbose_name="Telefon kontaktowy do magazynu", max_length=32)
    street = models.CharField(verbose_name="Ulica/Osiedle", max_length=128)
    home = models.CharField(verbose_name="Numer domu", max_length=8)
    door = models.CharField(
        verbose_name="Numer lokalu",
        max_length=8,
        null=True,
        blank=True,
    )
    city = models.CharField(verbose_name="Miasto",
                            max_length=64,
                            default="Kraków")
    post_code = models.CharField(verbose_name="Kod pocztowy",
                                 null=True,
                                 blank=True,
                                 max_length=6)
    info = models.CharField(verbose_name="Info",
                            max_length=256,
                            null=True,
                            blank=True)

    is_active = models.BooleanField(verbose_name="Czy jest aktywna",
                                    default=True)

    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    google_maps_link = models.TextField(verbose_name="Link z mapy google",
                                        null=True,
                                        blank=True)
    facebook_link = models.URLField(verbose_name="Link do facebook",
                                    null=True,
                                    blank=True)

    def products(self):
        return Products.objects.filter(store_id=self).filter(is_active=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Store, self).save()

    def get_absolute_url(self):
        return reverse("store_details", kwargs={
            "slug": self.slug,
        })

    class Meta:
        ordering = ("id", )
        verbose_name_plural = "Magazyn"

    def __str__(self):
        return "{}, {}".format(str(self.id), self.name)


class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    tag_desc = models.CharField(
        verbose_name="Meta description",
        max_length=156,
    )

    tag_title = models.CharField(
        verbose_name="Title",
        max_length=70,
    )
    number = models.IntegerField(verbose_name="Numer kategorii",
                                 null=True,
                                 blank=True,
                                 default=0)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              upload_to='images/categorys/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    name = models.CharField(verbose_name="Nazwa kategorii", max_length=128)
    text = models.TextField(verbose_name="Opis kategorii")
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    on_page = models.BooleanField(verbose_name="Czy na pierwszej stronie?",
                                  default=False)
    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def counter(self, workplace):
        return Products.objects.filter(category=self).filter(
            is_active=True).filter(store_id=workplace).count()

    def products(self):
        return Products.objects.filter(category=self).filter(is_active=True)

    def images_stamp(self):
        return Images.objects.filter(category_id=self).filter(stamp=True)

    class Meta:
        ordering = (
            "number",
            "name",
        )
        verbose_name_plural = "Kategorie produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def get_absolute_url(self):
        return reverse("category_details",
                       kwargs={
                           "category": self.slug,
                           "pk": self.id,
                       })

    def sub_category(self):
        return SubCategory.objects.filter(category=self)

    def __str__(self):
        return self.name

    @property
    def products_count(self):
        return Products.objects.filter(sub_category_type__sub_category__category=self).count()


class SubCategory(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa podkategorii", max_length=128)
    desc = models.TextField(
        verbose_name="Opis podkategorii", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        verbose_name="Kategoria podkategorii",
        on_delete=models.CASCADE,
        db_index=True,
    )
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    number = models.IntegerField(verbose_name="Numer kategorii",
                                 null=True,
                                 blank=True,
                                 default=0)
    image = models.ImageField(verbose_name="Zdjęcie główne",
                              upload_to='images/categorys/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)

    class Meta:
        ordering = (
            "category",
            "number",
            "name",
        )
        verbose_name_plural = "PodKategorie produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save()

    def get_absolute_url(self):
        return reverse("sub_category_details",
                       kwargs={
                           "sub_category": self.slug,
                           "pk": self.id,
                       })

    def sub_cat_type(self):
        return SubCategoryType.objects.filter(sub_category=self)

    def __str__(self):
        return self.name

    @property
    def products_count(self):
        return Products.objects.filter(sub_category_type__sub_category=self).count()


class SubCategoryType(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Nazwa rodzaje produktu w podkategorii", max_length=128)
    sub_category = models.ForeignKey(
        "SubCategory",
        verbose_name="Rodzaje produktów w podkategorii",
        on_delete=models.CASCADE,
        db_index=True,
    )
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    number = models.IntegerField(verbose_name="Numer wyświetlania",
                                 null=True,
                                 blank=True,
                                 default=0)
    image = models.ImageField(verbose_name="Zdjęcie główne",
                              upload_to='images/categorys/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)

    class Meta:
        ordering = (
            "sub_category",
            "number",
            "name",
        )
        verbose_name_plural = "Rodzaje produktów w podkategori"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategoryType, self).save()

    def get_absolute_url(self):
        return reverse("sub_category_type_details",
                       kwargs={
                           "category": self.sub_category.category.slug,
                           "sub_category": self.sub_category.slug,
                           "slug": self.slug,
                           "pk": self.id,
                       })

    def __str__(self):
        return self.sub_category.name + ", " + self.name

    @property
    def products_count(self):
        return Products.objects.filter(sub_category_type=self).count()


class Brand(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa marki", max_length=128)
    logo = models.ImageField(verbose_name="Zdjęcie główne",
                             upload_to='images/categorys/',
                             validators=[file_size],
                             null=True,
                             blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    desc = models.TextField(verbose_name="Brand info", blank=True, null=True)

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Marka produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save()

    def __str__(self):
        return self.name


class Size(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Rozmiar produktu (wielkość, pojemność, waga)",
        max_length=64)
    is_active = models.BooleanField(verbose_name="Czy jest aktualny",
                                    default=True)

    def products(self, workplace):
        return Products.objects.filter(size=self).filter(
            is_active=True).filter(store_id=workplace)

    def counter(self, workplace):
        return Products.objects.filter(size=self).filter(
            is_active=True).filter(store_id=workplace).count()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Rozmiary produktów"

    def __str__(self):
        return self.name


class Colors(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa koloru", max_length=32)
    class_text = models.CharField(
        verbose_name="Text dla koloru klasy",
        max_length=32,
    )
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Kolory"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Colors, self).save()

    def __str__(self):
        return self.name


class Vat(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(verbose_name="Stawka VAT")
    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def __str__(self):
        return "{}%".format(self.name)


class Products(BaseModel):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey("Store",
                              verbose_name="Magazyn",
                              on_delete=models.CASCADE,
                              db_index=True,
                              default=1)
    sub_category_type = models.ForeignKey(
        "SubCategoryType",
        verbose_name="Typ produktu",
        on_delete=models.CASCADE,
        db_index=True,
    )
    brand = models.ForeignKey("Brand",
                              verbose_name="Marka produktu",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    color = models.ForeignKey("Colors",
                              verbose_name="Kolor produktu",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    name = models.CharField(verbose_name="Nazwa produktu", max_length=128)
    code = models.CharField(
        verbose_name="Kod kreskowy", blank=True, null=True, max_length=8)
    qty = models.IntegerField(default=1,
                              verbose_name="Ilość produktu na stanie")
    size = models.ForeignKey('Size',
                             on_delete=models.CASCADE,
                             verbose_name="Rozmiar",
                             null=True,
                             blank=True)
    desc = models.TextField(verbose_name="Produkt info", blank=True, null=True)
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              upload_to='images/products/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    price = models.DecimalField(verbose_name="Cena podstawowa",
                                default=0,
                                decimal_places=2,
                                max_digits=7)
    discount = models.IntegerField(default=0, verbose_name="Rabat")
    price_promo = models.DecimalField(
        verbose_name="Cena promocyjna",
        default=0,
        decimal_places=2,
        max_digits=7,
        blank=True,
        null=True,
    )
    price_netto_purchase = models.DecimalField(verbose_name="Cena zakupu netto",
                                               default=0,
                                               decimal_places=2,
                                               max_digits=7,
                                               null=True,
                                               blank=True)
    price_netto = models.DecimalField(verbose_name="Cena netto",
                                      default=0,
                                      decimal_places=2,
                                      max_digits=7,
                                      null=True,
                                      blank=True)
    tax = models.ForeignKey(
        "Vat",
        on_delete=models.CASCADE,
        verbose_name="Stawka VAT",
    )
    is_recommended = models.BooleanField(verbose_name="Czy jest w rekomendowanych",
                                         default=False)

    is_news = models.BooleanField(verbose_name="Czy jest w nowościach",
                                  default=False)
    is_promo = models.BooleanField(verbose_name="Czy jest w propozycjach",
                                   default=False)

    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def other_colors(self):
        return Products.objects.filter(name=self.name).exclude(
            pk=self.pk).filter(is_active=True)

    def images(self):
        return Images.objects.filter(product_id=self)

    def get_absolute_url(self):
        return reverse("product_details",
                       kwargs={
                           "cat": self.sub_category_type.sub_category.category.slug,
                           "sub_cat": self.sub_category_type.sub_category.slug,
                           "sub_cat_type": self.sub_category_type.slug,
                           "product": self.slug,
                           "pk": self.id,

                       })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount > 0:
            self.price_promo = float(self.price) - \
                float(self.price) * (self.discount / 100)

        else:
            self.price_promo = self.price
        self.price_netto = float(self.price_promo) / \
            float("1." + str(self.tax.name))
        super(Products, self).save()

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Produkty"

    def __str__(self):
        return self.name

    @property
    def seo_tag_description(self):
        if self.brand:
            description = f"Produkt marki {self.brand.name}"
        else:
            description = f"Produkt {self.name}"
        return description


class Images(BaseModel):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/',
                              validators=[file_size])
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    category = models.ForeignKey("Category",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 verbose_name="Zdjęcia kategorii",
                                 related_name='category_gallery')
    product = models.ForeignKey("Products",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                verbose_name="Zdjęcie produktu",
                                related_name='product_gallery')
    main = models.BooleanField(verbose_name="Zdjęcie główne", default=False)
    stamp = models.BooleanField(verbose_name="Zdjęcie wzornika?",
                                default=False)
    carousel = models.BooleanField(verbose_name="Zdjęcie na karuzele?",
                                   default=False)
    description = models.TextField(verbose_name="Mały opis dla obrazka na karuzeli",
                                   blank=True,
                                   null=True,
                                   max_length=264)
    logo = models.BooleanField(verbose_name="Logo główne", default=False)

    class Meta:
        ordering = (
            '-id',
            "image",
        )
        verbose_name_plural = "Galeria"

    def save(self):
        im = Image.open(self.image)
        output = BytesIO()
        im.save(output, format='WEBP', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(
            output, 'ImageField', "%s.webp" % self.image.name.split('.')[0],
            'image/webp', sys.getsizeof(output), None)
        super(Images, self).save()

    def __str__(self):
        return str(self.id)
