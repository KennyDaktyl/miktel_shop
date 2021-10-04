# Generated by Django 3.2.7 on 2021-10-04 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0015_auto_20211001_1340'),
    ]

    operations = [
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
                'abstract': False,
            },
        ),
    ]
