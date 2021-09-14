# Generated by Django 3.2 on 2021-04-06 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=9, verbose_name='Numer telefonu')),
                ('nip_number', models.CharField(max_length=13, verbose_name='Numer nip')),
                ('company', models.BooleanField(default=False, verbose_name='Profil firmowy?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profil użytkownika',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(blank=True, max_length=128, null=True, verbose_name='Ulica')),
                ('house', models.CharField(max_length=8, verbose_name='Nr domu')),
                ('door', models.CharField(blank=True, max_length=8, null=True, verbose_name='Nr lokalu')),
                ('city', models.CharField(blank=True, default='Kraków', max_length=64, null=True, verbose_name='Miasto')),
                ('post_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Kod pocztowy')),
                ('main', models.BooleanField(default=False, verbose_name='Główny adres')),
                ('user_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name_plural': 'Adresy',
                'ordering': ('user_id',),
            },
        ),
    ]
