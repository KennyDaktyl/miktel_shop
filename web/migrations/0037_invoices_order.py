# Generated by Django 3.2.7 on 2022-02-18 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0036_auto_20220218_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.orders'),
        ),
    ]
