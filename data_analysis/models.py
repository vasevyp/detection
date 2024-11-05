from django.db import models
from django_pandas.managers import DataFrameManager
# from django.utils import timezone

class DoubleData(models.Model):
    """Class representing a total double data of energy"""
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
    
    class Meta:
        """Help total data"""
        ordering = ['-current_consumption']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'Равные данные по потреблению в несколких периодах'
        verbose_name_plural = 'Равные данные по потреблению в несколких периодах'

    def __str__(self):
        return str(self.period)  
    
    objects = DataFrameManager()
    
class Apartment(models.Model):
    '''Model for analyzing abnormally low/high (deviation more than 25%) heat energy consumption in apartment buildings'''
    subunit = models.CharField(max_length=30, verbose_name='Подразделение', null=True, blank = True)
    odpu_number = models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type = models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    # current_date = models.DateField(verbose_name='Дата текущего показания',
                                #   help_text="2022-08-01", null=True, blank = True)
    current_consumption =models.CharField(max_length=30, verbose_name='Текущее потребление, Гкал', null=True, blank = True)
    period = models.CharField(max_length=20,verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")
    floors = models.CharField(max_length=3, verbose_name='Этажность объекта',null=True, blank = True) #from basic.ObjectData
    construction_date = models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True) #from basic.ObjectData
    area =models.FloatField(verbose_name='Общая площадь объекта', null=True, blank = True) #from basic.ObjectData
    specific_data =models.FloatField(verbose_name='Удельное потребление, Гкал/1кв.м', null=True, blank = True)
    object_group = models.IntegerField(verbose_name='Группа объекта',null=True, blank = True)
    median_value_s = models.FloatField(verbose_name='Медиана удельных данных', null=True, blank = True)
    index_abnormal = models.FloatField(verbose_name='Индекс потребления от медианы: >25%(-1), <25%(1), другое (0)', null=True, blank = True)
    median_value_s_deviation = models.FloatField(verbose_name='Коэффициент отклонения от медианы', null=True, blank = True)
    created_date = models.DateField(
        auto_now_add=True, verbose_name='Создан', null=True)
    updated_date = models.DateField(
        auto_now=True,  verbose_name='Изменен', null=True)
    
    class Meta:
        """Help total data"""
        ordering = ['current_consumption']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'Apartment - Модель анализа потребления многоэтажками'
        verbose_name_plural = 'Apartment - Модель анализа потребления многоэтажками'

    def __str__(self):
        return str(self.period) 
    
    # def save(self, *args, **kwargs):
    #     if self.period:
    #         # Convert date to string before passing to fromisoformat function
    #         self.period = timezone.datetime.strftime(self.period, '%Y-%m-%d')
    #     super().save(*args, **kwargs)


    
    # @property
    # def specific_data(self):
    #     if self.area == 0:
    #         return 0 
    #     return self.current_consumption/self.area       
         
    
    
    objects = DataFrameManager()

class ObjectDataReport(models.Model):
    """Class representing data of heat energy consumer objects from report"""
    address = models.CharField(max_length=100, verbose_name='Адрес объекта', null=True, blank = True)
    object_type =models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    floors = models.CharField(max_length=50, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date = models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area =models.CharField(max_length=30, verbose_name='Общая площадь объекта', null=True, blank = True)
    # subunit = models.CharField(max_length=30, verbose_name='Подразделение', null=True, blank = True)
    # odpu_number = models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    # energy_type = models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    created_date = models.DateField(
        auto_now_add=True, verbose_name='Создан', null=True)
    updated_date = models.DateField(
        auto_now=True,  verbose_name='Изменен', null=True)
    class Meta:
        """Help object data"""
        ordering = ['address']
        verbose_name = 'Данные по объекту с учетом отчета потребления'
        verbose_name_plural = 'Данные по объектам с учетом отчетов потребления'

    def __str__(self):
        return str(self.address)   
    
