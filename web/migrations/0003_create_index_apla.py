from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_citys_index_alfa'),
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
                ('city_five', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_five', to='web.citys')),
                ('city_four', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_four', to='web.citys')),
                ('city_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_one', to='web.citys')),
                ('city_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_three', to='web.citys')),
                ('city_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_two', to='web.citys')),
            ],
            options={
                'verbose_name_plural': 'Index alpfa',
                'ordering': ('name',),
            }
)
]


