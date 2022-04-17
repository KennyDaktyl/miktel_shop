# Generated by Django 4.0.3 on 2022-04-17 22:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_citys_indexalfa'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexAlfaStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Nazwa miejscowości')),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Slug')),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla indexu')),
                ('meta_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla indexu')),
            ],
            options={
                'verbose_name_plural': 'Index alpfa',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='citys',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Meta description dla miasta'),
        ),
        migrations.AddField(
            model_name='citys',
            name='meta_title',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Meta title dla miasta'),
        ),
        migrations.DeleteModel(
            name='IndexAlfa',
        ),
        migrations.AddField(
            model_name='indexalfastamp',
            name='city_five',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_five', to='web.citys'),
        ),
        migrations.AddField(
            model_name='indexalfastamp',
            name='city_four',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_four', to='web.citys'),
        ),
        migrations.AddField(
            model_name='indexalfastamp',
            name='city_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_one', to='web.citys'),
        ),
        migrations.AddField(
            model_name='indexalfastamp',
            name='city_three',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_three', to='web.citys'),
        ),
        migrations.AddField(
            model_name='indexalfastamp',
            name='city_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_two', to='web.citys'),
        ),
    ]
