# Generated by Django 3.2.7 on 2023-03-23 11:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import uuid
import web.models.articles
import web.models.images
import web.models.products


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=128, verbose_name='Ulica')),
                ('house', models.CharField(max_length=8, verbose_name='Nr domu')),
                ('door', models.CharField(blank=True, max_length=8, null=True, verbose_name='Nr lokalu')),
                ('city', models.CharField(max_length=64, verbose_name='Miasto')),
                ('post_code', models.CharField(max_length=6, verbose_name='Kod pocztowy')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name_plural': 'Adresy',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256, verbose_name='Tytyuł artykułu')),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='Treść artukułu')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[1280, 960], upload_to='images/articles/', validators=[web.models.articles.file_size], verbose_name='Zdjęcie główne')),
                ('image_alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('image_title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla artykułu')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla artykułu')),
            ],
            options={
                'verbose_name_plural': 'Artykuły',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa marki')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/categorys/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Brand info')),
            ],
            options={
                'verbose_name_plural': 'Marka produktów',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_desc', models.CharField(max_length=156, verbose_name='Meta description')),
                ('tag_title', models.CharField(max_length=70, verbose_name='Title')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Numer kategorii')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[1280, 960], upload_to='images/categorys/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa kategorii')),
                ('text', models.TextField(verbose_name='Opis kategorii')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('on_page', models.BooleanField(default=False, verbose_name='Czy na pierwszej stronie?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy jest dostępny')),
            ],
            options={
                'verbose_name_plural': 'Kategorie produktów',
                'ordering': ('number', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Citys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Nazwa miejscowości')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('rybna_area', models.BooleanField(default=False, verbose_name='Okolica Rybnej')),
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla miasta')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla miasta')),
            ],
            options={
                'verbose_name_plural': 'Miasta',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='Nazwa koloru')),
                ('class_text', models.CharField(blank=True, max_length=32, null=True, verbose_name='Text dla koloru klasy')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name_plural': 'Kolory',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='Numer wyświetlania')),
                ('id_code', models.CharField(max_length=64, verbose_name='Kod dla id iframe inposta')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa metody płatności')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena za dostawę')),
                ('price_promo', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena promocyjna')),
                ('price_netto', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena netto')),
                ('default', models.BooleanField(default=False, verbose_name='Czy domyślny?')),
                ('inpost_box', models.BooleanField(default=False, verbose_name='Czy dostawa to paczkomat?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy aktualna?')),
            ],
            options={
                'verbose_name_plural': 'Rodzaje dostawy',
                'ordering': ('-number',),
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('number', models.CharField(max_length=64)),
                ('override_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='Nadpisany numer faktury')),
                ('override_date', models.DateField(blank=True, null=True, verbose_name='Nadpisana data faktury')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Faktury',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=64, verbose_name='Numer zamówienia')),
                ('pay_status', models.IntegerField(choices=[(1, 'Otwarte'), (2, 'Do zapłaty'), (3, 'Zapłacone')], default=1, verbose_name='Status płatności')),
                ('status', models.IntegerField(choices=[(1, 'Otwarte'), (2, 'W przygotowaniu'), (3, 'W dostawie'), (4, 'Gotowe do odbioru'), (5, 'Zrealizowane'), (6, 'Anulowane')], default=1, verbose_name='Status zamówienia')),
                ('payment_intent', models.CharField(blank=True, max_length=32, null=True, verbose_name='Id płatności w Stripe')),
                ('payment_success', models.BooleanField(default=False, verbose_name='Elektroniczna płatność udana')),
                ('inpost_box', models.CharField(blank=True, max_length=64, null=True, verbose_name='Numer paczkomatu')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Numer telefonu')),
                ('start_delivery_time', models.TimeField(blank=True, null=True, verbose_name='Czas wywozu')),
                ('sms_send', models.BooleanField(default=False, verbose_name='Sms')),
                ('sms_time', models.TimeField(blank=True, null=True, verbose_name='Czas smsa')),
                ('promo', models.BooleanField(default=False, verbose_name='Promocja')),
                ('discount', models.IntegerField(default=0, verbose_name='Rabat')),
                ('info', models.CharField(blank=True, max_length=256, null=True, verbose_name='Informacje')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena zamówienia')),
                ('products_item', models.JSONField(blank=True, null=True, verbose_name='Produkty')),
                ('invoice_true', models.BooleanField(default=False, verbose_name='Czy wybrano fakturę')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.address', verbose_name='Adres dostawy')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinet_id', to=settings.AUTH_USER_MODEL, verbose_name='Klient')),
                ('delivery_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.deliverymethod', verbose_name='Rodzaj dostawy')),
                ('invoice', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.invoices', verbose_name='Faktura')),
            ],
            options={
                'verbose_name_plural': 'Zamówienia',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='Numer wyświetlania')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa metody płatności')),
                ('pay_method', models.IntegerField(choices=[(1, 'gotówka'), (2, 'karta'), (3, 'przelew'), (4, 'przelew p24')], verbose_name='Rodzaj płatności')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[1280, 960], upload_to='images/products/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link do regulaminu')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena zamówienia')),
                ('default', models.BooleanField(default=False, verbose_name='Czy domyślny?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy aktualna')),
            ],
            options={
                'verbose_name_plural': 'Rodzaje płatności',
                'ordering': ('-number',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Rozmiar produktu (wielkość, pojemność, waga)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy jest aktualny')),
            ],
            options={
                'verbose_name_plural': 'Rozmiary produktów',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa magazynu')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[1280, 960], upload_to='images/workplace/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('phone_number', models.CharField(max_length=32, verbose_name='Telefon kontaktowy do magazynu')),
                ('street', models.CharField(max_length=128, verbose_name='Ulica/Osiedle')),
                ('home', models.CharField(max_length=8, verbose_name='Numer domu')),
                ('door', models.CharField(blank=True, max_length=8, null=True, verbose_name='Numer lokalu')),
                ('city', models.CharField(default='Kraków', max_length=64, verbose_name='Miasto')),
                ('post_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Kod pocztowy')),
                ('info', models.CharField(blank=True, max_length=256, null=True, verbose_name='Info')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy jest aktywna')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('google_maps_link', models.TextField(blank=True, null=True, verbose_name='Link z mapy google')),
                ('facebook_link', models.URLField(blank=True, null=True, verbose_name='Link do facebook')),
            ],
            options={
                'verbose_name_plural': 'Magazyn',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa podkategorii')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Numer kategorii')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/categorys/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla kategorii')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla kategorii')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Opis podkategorii')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category', verbose_name='Kategoria podkategorii')),
            ],
            options={
                'verbose_name_plural': 'PodKategorie produktów',
                'ordering': ('category', 'number', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Vat',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.IntegerField(verbose_name='Stawka VAT')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy jest dostępny')),
            ],
            options={
                'verbose_name_plural': 'Podatek Vat',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SubCategoryType',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa rodzaje produktu w podkategorii')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Numer wyświetlania')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/categorys/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla podkategorii')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla podkategorii')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.subcategory', verbose_name='Rodzaje produktów w podkategorii')),
            ],
            options={
                'verbose_name_plural': 'Rodzaje produktów w podkategori',
                'ordering': ('sub_category', 'number', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=18, verbose_name='Numer telefonu')),
                ('nip_number', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='Numer nip')),
                ('company_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nazwa firmy')),
                ('company_name_l', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nazwa firmy c.d.')),
                ('company', models.BooleanField(default=False, verbose_name='Profil firmowy?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profil użytkownika',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Nazwa produktu')),
                ('code', models.CharField(blank=True, max_length=8, null=True, verbose_name='Kod kreskowy')),
                ('qty', models.IntegerField(default=1, verbose_name='Ilość produktu na stanie')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Produkt info')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla produktu')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla produktu')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[800, 600], upload_to='images/products/', validators=[web.models.products.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Cena podstawowa')),
                ('discount', models.IntegerField(default=0, verbose_name='Rabat')),
                ('price_promo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True, verbose_name='Cena promocyjna')),
                ('price_netto_purchase', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True, verbose_name='Cena zakupu netto')),
                ('price_netto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True, verbose_name='Cena netto')),
                ('is_top', models.BooleanField(db_index=True, default=False, verbose_name='Czy jest w top')),
                ('is_recommended', models.BooleanField(db_index=True, default=False, verbose_name='Czy jest w rekomendowanych')),
                ('is_news', models.BooleanField(default=False, verbose_name='Czy jest w nowościach')),
                ('is_promo', models.BooleanField(db_index=True, default=False, verbose_name='Czy jest w propozycjach')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy jest dostępny')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.brand', verbose_name='Marka produktu')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.colors', verbose_name='Kolor produktu')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.size', verbose_name='Rozmiar')),
                ('store', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.store', verbose_name='Magazyn')),
                ('sub_category_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.subcategorytype', verbose_name='Typ produktu')),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.vat', verbose_name='Stawka VAT')),
            ],
            options={
                'verbose_name_plural': 'Produkty',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductCopy',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(verbose_name='Ilość pozycji')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Cena podstawowa')),
                ('discount', models.IntegerField(default=0, verbose_name='Rabat')),
                ('info', models.CharField(blank=True, max_length=256, null=True, verbose_name='Informacje')),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.orders', verbose_name='Relacja do zamówienia')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.products', verbose_name='Relacja do produktu')),
            ],
            options={
                'verbose_name_plural': 'Pozycje rachunku',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='pay_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.paymethod', verbose_name='Rodzaj płatności'),
        ),
        migrations.AddField(
            model_name='orders',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.store', verbose_name='Magazyn'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.orders'),
        ),
        migrations.CreateModel(
            name='IndexAlfaStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Nazwa miejscowości')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla indexu')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla indexu')),
                ('city_five', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_five', to='web.citys')),
                ('city_four', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_four', to='web.citys')),
                ('city_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_one', to='web.citys')),
                ('city_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_three', to='web.citys')),
                ('city_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_two', to='web.citys')),
            ],
            options={
                'verbose_name_plural': 'Index alfabetyczny',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, size=[800, 600], upload_to='images/gallery/', validators=[web.models.images.file_size], verbose_name='Zdjęcie główne')),
                ('alt', models.CharField(blank=True, max_length=125, null=True, verbose_name='Alternatywny text dla obrazka')),
                ('title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title dla obrazka')),
                ('main', models.BooleanField(default=False, verbose_name='Zdjęcie główne')),
                ('stamp', models.BooleanField(default=False, verbose_name='Zdjęcie wzornika?')),
                ('carousel', models.BooleanField(default=False, verbose_name='Zdjęcie na karuzele?')),
                ('description', models.TextField(blank=True, max_length=264, null=True, verbose_name='Mały opis dla obrazka na karuzeli')),
                ('logo', models.BooleanField(default=False, verbose_name='Logo główne')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles_gallery', to='web.articles', verbose_name='Zdjęcie dla artykułu')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_gallery', to='web.category', verbose_name='Zdjęcia kategorii')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_gallery', to='web.products', verbose_name='Zdjęcie na galerie')),
            ],
            options={
                'verbose_name_plural': 'Galeria',
                'ordering': ('-id', 'image'),
            },
        ),
        migrations.AddField(
            model_name='citys',
            name='alphabetical_index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.indexalfastamp', verbose_name='alphabetical_index'),
        ),
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category', verbose_name='Kategoria artykułu'),
        ),
        migrations.CreateModel(
            name='ActivateToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('activation_token', models.CharField(max_length=64, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Token aktywacyjny',
                'ordering': ('-id',),
            },
        ),
    ]
