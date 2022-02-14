# Generated by Django 3.2.7 on 2021-09-21 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("web", "0002_brand_category_colors_images_products_size_store_vat"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryMethod",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "number",
                    models.IntegerField(verbose_name="Numer wyświetlania"),
                ),
                (
                    "id_code",
                    models.CharField(
                        max_length=64, verbose_name="Kod dla id iframe inposta"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=64, verbose_name="Nazwa metody płatności"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=7,
                        verbose_name="Cena za dostawę",
                    ),
                ),
                (
                    "price_promo",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=7,
                        verbose_name="Cena promocyjna",
                    ),
                ),
                (
                    "default",
                    models.BooleanField(
                        default=False, verbose_name="Czy domyślny?"
                    ),
                ),
                (
                    "inpost_box",
                    models.BooleanField(
                        default=False, verbose_name="Czy dostawa to paczkomat?"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Czy aktualna?"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Rodzaje dostawy",
                "ordering": ("number",),
            },
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "number",
                    models.CharField(
                        max_length=64, verbose_name="Numer zamówienia"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Otwarte"),
                            (2, "W przygotowaniu"),
                            (3, "W dostawie"),
                            (4, "Zrealizowane"),
                            (5, "Anulowane"),
                        ],
                        default=1,
                        verbose_name="Status zamówienia",
                    ),
                ),
                ("date", models.DateTimeField(db_index=True)),
                (
                    "delivery_method",
                    models.CharField(
                        max_length=64, verbose_name="Rodzaj dostawy"
                    ),
                ),
                (
                    "inpost_box",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Numer paczkomatu",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=12,
                        null=True,
                        verbose_name="Numer telefonu",
                    ),
                ),
                (
                    "pay_method",
                    models.CharField(
                        max_length=64, verbose_name="Rodzaj płatności"
                    ),
                ),
                (
                    "start_delivery_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Czas wywozu"
                    ),
                ),
                (
                    "sms_send",
                    models.BooleanField(default=False, verbose_name="Sms"),
                ),
                (
                    "sms_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Czas smsa"
                    ),
                ),
                (
                    "promo",
                    models.BooleanField(default=False, verbose_name="Promocja"),
                ),
                (
                    "discount",
                    models.IntegerField(default=0, verbose_name="Rabat"),
                ),
                (
                    "info",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Informacje",
                    ),
                ),
                (
                    "is_paid",
                    models.BooleanField(
                        default=False, verbose_name="Czy zapłacono?"
                    ),
                ),
                (
                    "printed",
                    models.BooleanField(
                        default=True, verbose_name="Wydrukowano paragon?"
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=7,
                        verbose_name="Cena zamówienia",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.address",
                        verbose_name="Adres dostawy",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clinet_id",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Klient",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.store",
                        verbose_name="Magazyn",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Zamówienia",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="PayMethod",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "number",
                    models.IntegerField(verbose_name="Numer wyświetlania"),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=64, verbose_name="Nazwa metody płatności"
                    ),
                ),
                (
                    "pay_method",
                    models.IntegerField(
                        choices=[(1, "gotówka"), (2, "karta"), (3, "przelew")],
                        verbose_name="Rodzaj płatności",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=7,
                        verbose_name="Cena zamówienia",
                    ),
                ),
                (
                    "default",
                    models.BooleanField(
                        default=False, verbose_name="Czy domyślny?"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Czy aktualna"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Rodzaje płatności",
                "ordering": ("number",),
            },
        ),
        migrations.AddField(
            model_name="products",
            name="discount",
            field=models.IntegerField(default=0, verbose_name="Rabat"),
        ),
        migrations.AddField(
            model_name="products",
            name="is_news",
            field=models.BooleanField(
                default=False, verbose_name="Czy jest w nowościach"
            ),
        ),
        migrations.CreateModel(
            name="ProductCopy",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "color_text",
                    models.IntegerField(
                        choices=[
                            (1, "Czarne"),
                            (2, "Czerwone"),
                            (3, "Niebieskie"),
                            (4, "Zielone"),
                            (5, "Fioletowe"),
                        ],
                        verbose_name="Kolor odbicia",
                    ),
                ),
                ("qty", models.IntegerField(verbose_name="Ilość pozycji")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=7,
                        verbose_name="Cena podstawowa",
                    ),
                ),
                (
                    "discount",
                    models.IntegerField(default=0, verbose_name="Rabat"),
                ),
                (
                    "info",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Informacje",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.orders",
                        verbose_name="Relacja do zamówienia",
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.products",
                        verbose_name="Relacja do produktu",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Pozycje rachunku",
                "ordering": ("-id",),
            },
        ),
    ]
