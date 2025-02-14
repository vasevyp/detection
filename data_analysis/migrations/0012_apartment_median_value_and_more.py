# Generated by Django 4.2.16 on 2024-10-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0011_alter_apartment_floors'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='median_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Медиана потребления по группе'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='median_value_deviation',
            field=models.FloatField(blank=True, null=True, verbose_name='Отклонение от медианы'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='median_value_s',
            field=models.FloatField(blank=True, null=True, verbose_name='Медиана удельных данных'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='median_value_s_deviation',
            field=models.FloatField(blank=True, null=True, verbose_name='Отклонение от медианы удельных данных'),
        ),
    ]
