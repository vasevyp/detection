# Generated by Django 4.2.16 on 2024-10-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energydata',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес объекта'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='current_consumption',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Текущее потребление, Гкал'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='current_date',
            field=models.DateField(blank=True, help_text='2022-08-01', null=True, verbose_name='Дата текущего показания'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='energy_type',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Вид энерг-а ГВС'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='object_type',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Тип объекта'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='odpu_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='№ ОДПУ'),
        ),
        migrations.AlterField(
            model_name='energydata',
            name='subunit',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Подразделение'),
        ),
    ]
