# Generated by Django 4.2.16 on 2024-11-02 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthResultMl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес объекта 2')),
                ('object_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Тип объекта')),
                ('odpu_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='№ ОДПУ')),
                ('energy_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Вид энерг-а ГВС')),
                ('floors', models.CharField(blank=True, max_length=3, null=True, verbose_name='Этажность объекта')),
                ('construction_date', models.CharField(blank=True, help_text='2022-08-01', max_length=20, null=True, verbose_name='Дата постройки')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Общая площадь объекта')),
                ('floors_group', models.CharField(blank=True, max_length=20, null=True, verbose_name='Группа этажность')),
                ('construction_group', models.CharField(blank=True, max_length=20, null=True, verbose_name='Группа год постройки')),
                ('current_consumption', models.CharField(blank=True, max_length=30, null=True, verbose_name='Потребление за период, Гкал')),
                ('specific_data', models.FloatField(blank=True, null=True, verbose_name='Удельное потребление, Гкал/1кв.м')),
                ('t_squared', models.FloatField(blank=True, null=True, verbose_name="Hotelling's T-squared")),
                ('q_residuals', models.FloatField(blank=True, null=True, verbose_name='Q residuals')),
                ('below_median', models.BooleanField(blank=True, null=True, verbose_name='Ниже медианы')),
                ('median_below25', models.BooleanField(blank=True, null=True, verbose_name='25% ниже медианы')),
                ('median_above25', models.BooleanField(blank=True, null=True, verbose_name='25% выше медианы')),
                ('period', models.CharField(help_text='2022-08-01', max_length=20, verbose_name='Период (мес, год)')),
            ],
            options={
                'verbose_name': 'MonthResultMl - результатов рассчета ML-модели за месяц',
                'verbose_name_plural': 'MonthResultMl - результатов рассчета ML-модели за месяц',
                'ordering': ['address2'],
            },
        ),
        migrations.CreateModel(
            name='ResultMl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес объекта 2')),
                ('object_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Тип объекта')),
                ('odpu_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='№ ОДПУ')),
                ('energy_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='Вид энерг-а ГВС')),
                ('floors', models.CharField(blank=True, max_length=3, null=True, verbose_name='Этажность объекта')),
                ('construction_date', models.CharField(blank=True, help_text='2022-08-01', max_length=20, null=True, verbose_name='Дата постройки')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Общая площадь объекта')),
                ('floors_group', models.CharField(blank=True, max_length=20, null=True, verbose_name='Группа этажность')),
                ('construction_group', models.CharField(blank=True, max_length=20, null=True, verbose_name='Группа год постройки')),
                ('current_consumption', models.CharField(blank=True, max_length=30, null=True, verbose_name='Потребление за период, Гкал')),
                ('specific_data', models.FloatField(blank=True, null=True, verbose_name='Удельное потребление, Гкал/1кв.м')),
                ('t_squared', models.FloatField(blank=True, null=True, verbose_name="Hotelling's T-squared")),
                ('q_residuals', models.FloatField(blank=True, null=True, verbose_name='Q residuals')),
                ('below_median', models.BooleanField(blank=True, null=True, verbose_name='Ниже медианы')),
                ('median_below25', models.BooleanField(blank=True, null=True, verbose_name='25% ниже медианы')),
                ('median_above25', models.BooleanField(blank=True, null=True, verbose_name='25% выше медианы')),
                ('period', models.CharField(help_text='2022-08-01', max_length=20, verbose_name='Период (мес, год)')),
            ],
            options={
                'verbose_name': 'ResultMl - Модель результатов рассчета ML-модели',
                'verbose_name_plural': 'ResultMl - Модель результатов рассчета ML-модели',
                'ordering': ['-period'],
            },
        ),
    ]
