from django.db import models
from django_pandas.managers import DataFrameManager


class MonthResultMl(models.Model):
    address2=models.CharField(max_length=100, verbose_name='Адрес объекта 2', null=True, blank = True)
    object_type=models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    odpu_number=models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type=models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    floors=models.CharField(max_length=3, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date=models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area=models.FloatField(verbose_name='Общая площадь объекта', null=True, blank = True)
    floors_group=models.CharField(max_length=20,verbose_name='Группа этажность',null=True, blank = True)
    construction_group=models.CharField(max_length=20,verbose_name='Группа год постройки',null=True, blank = True)
    current_consumption=models.CharField(max_length=30, verbose_name='Потребление за период, Гкал', null=True, blank = True)
    specific_data=models.FloatField(verbose_name='Удельное потребление, Гкал/1кв.м', null=True, blank = True)
    t_squared=models.FloatField(verbose_name="Hotelling's T-squared", null=True, blank = True)
    q_residuals=models.FloatField(verbose_name='Q residuals', null=True, blank = True)
    below_median=models.BooleanField(verbose_name='Ниже медианы', null=True, blank = True)
    median_below25=models.BooleanField(verbose_name='25% ниже медианы', null=True, blank = True)
    median_above25=models.BooleanField(verbose_name='25% выше медианы', null=True, blank = True)
    period=models.CharField(max_length=20,verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")

    class Meta:
        """Help total data"""
        ordering = ['address2']
        verbose_name = 'MonthResultMl - результатов рассчета ML-модели за месяц'
        verbose_name_plural = 'MonthResultMl - результатов рассчета ML-модели за месяц'

    def __str__(self):
        return str(self.period) 
    objects = DataFrameManager()

class ResultMl(models.Model):
    address2=models.CharField(max_length=100, verbose_name='Адрес объекта 2', null=True, blank = True)
    object_type=models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    odpu_number=models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type=models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    floors=models.CharField(max_length=3, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date=models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area=models.FloatField(verbose_name='Общая площадь объекта', null=True, blank = True)
    floors_group=models.CharField(max_length=20,verbose_name='Группа этажность',null=True, blank = True)
    construction_group=models.CharField(max_length=20,verbose_name='Группа год постройки',null=True, blank = True)
    current_consumption=models.CharField(max_length=30, verbose_name='Потребление за период, Гкал', null=True, blank = True)
    specific_data=models.FloatField(verbose_name='Удельное потребление, Гкал/1кв.м', null=True, blank = True)
    t_squared=models.FloatField(verbose_name="Hotelling's T-squared", null=True, blank = True)
    q_residuals=models.FloatField(verbose_name='Q residuals', null=True, blank = True)
    below_median=models.BooleanField(verbose_name='Ниже медианы', null=True, blank = True)
    median_below25=models.BooleanField(verbose_name='25% ниже медианы', null=True, blank = True)
    median_above25=models.BooleanField(verbose_name='25% выше медианы', null=True, blank = True)
    period=models.CharField(max_length=20,verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")

    class Meta:
        """Help total data"""
        ordering = ['-period']
        # unique_together= ('period','odpu_number', 'current_consumption')
        verbose_name = 'ResultMl - Модель результатов рассчета ML-модели'
        verbose_name_plural = 'ResultMl - Модель результатов рассчета ML-модели'

    def __str__(self):
        return str(self.period) 
    
class TempAnomalData(models.Model):
    address2=models.CharField(max_length=100, verbose_name='Адрес объекта 2', null=True, blank = True)
    object_type=models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    odpu_number=models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type=models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    floors=models.CharField(max_length=3, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date=models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area=models.FloatField(verbose_name='Общая площадь объекта', null=True, blank = True)
    floors_group=models.CharField(max_length=20,verbose_name='Группа этажность',null=True, blank = True)
    construction_group=models.CharField(max_length=20,verbose_name='Группа год постройки',null=True, blank = True)
    current_consumption=models.CharField(max_length=30, verbose_name='Потребление за период, Гкал', null=True, blank = True)
    specific_data=models.FloatField(verbose_name='Удельное потребление, Гкал/1кв.м', null=True, blank = True)
    t_squared=models.FloatField(verbose_name="Hotelling's T-squared", null=True, blank = True)
    q_residuals=models.FloatField(verbose_name='Q residuals', null=True, blank = True)
    below_median=models.BooleanField(verbose_name='Ниже медианы', null=True, blank = True)
    median_below25=models.BooleanField(verbose_name='25% ниже медианы', null=True, blank = True)
    median_above25=models.BooleanField(verbose_name='25% выше медианы', null=True, blank = True)
    period=models.CharField(max_length=20,verbose_name='Период (мес, год)',
                                  help_text="2022-08-01")

    class Meta:
        """Help total data"""
        ordering = ['-period']
        verbose_name = 'TempAnomalData - Модель выборки результатов рассчета ML-модели'
        verbose_name_plural = 'TempAnomalData - Модель выборки результатов рассчета ML-модели'

    def __str__(self):
        return str(self.period)     



class ForecastData(models.Model):
    address2=models.CharField(max_length=100, verbose_name='Адрес объекта 2', null=True, blank = True)
    object_type=models.CharField(max_length=30, verbose_name='Тип объекта', null=True, blank = True)
    odpu_number=models.CharField(max_length=50, verbose_name='№ ОДПУ',null=True, blank = True)
    energy_type=models.CharField(max_length=30, verbose_name='Вид энерг-а ГВС', null=True, blank = True)
    floors=models.CharField(max_length=3, verbose_name='Этажность объекта',null=True, blank = True)
    construction_date=models.CharField(max_length=20,verbose_name='Дата постройки',
                                  help_text="2022-08-01", null=True, blank = True)
    area=models.FloatField(verbose_name='Общая площадь объекта', null=True, blank = True)
    period=models.CharField(max_length=20,verbose_name='Период (мес, год)',help_text="2022-08-01")
    
    forecast_index=models.FloatField(verbose_name='Индекс прогноза удельного потребления', null=True, blank = True)
    specific_data=models.FloatField(verbose_name='Удельное потребление, Гкал/1кв.м', null=True, blank = True)
    forecast=models.FloatField(verbose_name='Прогноз удельного потребления, Гкал/1кв.м', null=True, blank = True)
    forecast_deviation=models.FloatField(verbose_name='Коэффициент (прогноз/факт) удельного потребления', null=True, blank = True)

    class Meta:
        """Help total data"""
        ordering = ['-period']
        verbose_name = 'Прогноз потребления - Модель выборки результатов рассчета ML-модели'
        verbose_name_plural = 'Прогноз потребления - Модель выборки результатов рассчета ML-модели'

    def __str__(self):
        return str(self.period)     
