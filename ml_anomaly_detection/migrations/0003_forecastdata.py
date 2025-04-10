# Generated by Django 4.2.16 on 2024-11-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_anomaly_detection', '0002_tempanomaldata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес объекта 2')),
                ('object_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Тип объекта')),
                ('odpu_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='№ ОДПУ')),
                ('energy_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Вид энерг-а ГВС')),
                ('floors', models.CharField(blank=True, max_length=3, null=True, verbose_name='Этажность объекта')),
                ('construction_date', models.CharField(blank=True, help_text='2022-08-01', max_length=20, null=True, verbose_name='Дата постройки')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Общая площадь объекта')),
                ('period', models.CharField(help_text='2022-08-01', max_length=20, verbose_name='Период (мес, год)')),
                ('forecast_index', models.FloatField(blank=True, null=True, verbose_name='Индекс прогноза удельного потребления')),
                ('specific_data', models.FloatField(blank=True, null=True, verbose_name='Удельное потребление, Гкал/1кв.м')),
                ('forecast', models.FloatField(blank=True, null=True, verbose_name='Прогноз удельного потребления, Гкал/1кв.м')),
                ('forecast_deviation', models.FloatField(blank=True, null=True, verbose_name='коэффициент (прогноза/факт) удельного потребления')),
            ],
            options={
                'verbose_name': 'Прогноз потребления - Модель выборки результатов рассчета ML-модели',
                'verbose_name_plural': 'Прогноз потребления - Модель выборки результатов рассчета ML-модели',
                'ordering': ['-period'],
            },
        ),
    ]
