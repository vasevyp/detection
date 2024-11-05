"""Basic data module for analysis"""
from django.db import models
from django_pandas.managers import DataFrameManager

class EnergyData(models.Model):
    """Class representing a month data of energy"""
    subunit = models.CharField(max_length=30, verbose_name='Подразделение', null=True, blank = True)
    odpu_number = models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type = models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    current_date = models.DateField(verbose_name='Дата текущего показания',
                                  help_text="2022-08-01", null=True, blank = True)
    current_consumption =models.CharField(max_length=30, verbose_name='Текущее потребление, Гкал', null=True, blank = True)
    period = models.DateField(verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")
    generated_by= models.CharField(max_length=50, verbose_name='Сформировал')
    created_date = models.DateField(verbose_name='Создан', null=True)
    class Meta:
        """Help month data"""
        ordering = ['-period']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'Данные по потреблению тепловой энергии за последний месяц'
        verbose_name_plural = 'Данные по потреблению тепловой энергии за последний месяц'

    def __str__(self):
        return str(self.period)

class EnergyDataTotal(models.Model):
    """Class representing a total data of energy"""
    subunit = models.CharField(max_length=30, verbose_name='Подразделение', null=True, blank = True)
    odpu_number = models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type = models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    current_date = models.DateField(verbose_name='Дата текущего показания',
                                  help_text="2022-08-01", null=True, blank = True)
    current_consumption =models.CharField(max_length=30, verbose_name='Текущее потребление, Гкал', null=True, blank = True)
    period = models.DateField(verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")
    generated_by= models.CharField(max_length=50, verbose_name='Сформировал')
    created_date = models.DateField(verbose_name='Создан', null=True)
    class Meta:
        """Help total data"""
        ordering = ['-period']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'Исторические данные по потреблению тепловой энергии'
        verbose_name_plural = 'Исторические данные по потреблению тепловой энергии'

    def __str__(self):
        return str(self.period)  
    
    objects = DataFrameManager()
class AnomalEnergyData(models.Model):
    """Class representing a total anomal data of energy"""
    subunit = models.CharField(max_length=30, verbose_name='Подразделение', null=True, blank = True)
    odpu_number = models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type = models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    current_date = models.DateField(verbose_name='Дата текущего показания',
                                  help_text="2022-08-01", null=True, blank = True)
    current_consumption =models.CharField(max_length=30, verbose_name='Текущее потребление, Гкал', null=True, blank = True)
    period = models.DateField(verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")
    generated_by= models.CharField(max_length=50, verbose_name='Сформировал')
    created_date = models.DateField(verbose_name='Создан', null=True)
    class Meta:
        """Help total data"""
        ordering = ['-period']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'Аномальные данные по потреблению тепловой энергии'
        verbose_name_plural = 'Аномальные данные по потреблению тепловой энергии'

    def __str__(self):
        return str(self.period)         

class ObjectDataLoad(models.Model):
    """Class, loading data of objects-consumers of thermal energy"""
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    floors = models.CharField(max_length=50, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date = models.CharField(max_length=15, verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area =models.CharField(max_length=30, verbose_name='Площадь объекта', null=True, blank = True)

    created_date = models.DateField(
        auto_now_add=True, verbose_name='Создан', null=True)
    updated_date = models.DateField(
        auto_now=True,  verbose_name='Изменен', null=True)
    class Meta:
        """Help object data"""
        ordering = ['address']
        verbose_name = 'Загрузка объекта '
        verbose_name_plural = 'Загрузки по объектам'

    def __str__(self):
        return str(self.address)  


class ObjectData(models.Model):
    """Class representing data of heat energy consumer objects"""
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    floors = models.CharField(max_length=50, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date = models.CharField(max_length=15, verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area =models.CharField(max_length=30, verbose_name='Общая площадь объекта', null=True, blank = True)
    object_area =models.CharField(max_length=30, verbose_name='Площадь объекта', null=True, blank = True)

    created_date = models.DateField(
        auto_now_add=True, verbose_name='Создан', null=True)
    updated_date = models.DateField(
        auto_now=True,  verbose_name='Изменен', null=True)
    
    class Meta:
        """Help object data"""
        ordering = ['address']
        verbose_name = 'Данные по объекту '
        verbose_name_plural = 'Данные по объектам'

    def __str__(self):
        return str(self.address)   

