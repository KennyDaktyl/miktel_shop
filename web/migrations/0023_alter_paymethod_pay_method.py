# Generated by Django 3.2.7 on 2021-10-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0022_paymethod_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymethod",
            name="pay_method",
            field=models.IntegerField(
                choices=[
                    (1, "gotówka"),
                    (2, "karta"),
                    (3, "przelew"),
                    (4, "p24"),
                ],
                verbose_name="Rodzaj płatności",
            ),
        ),
    ]
