from django import forms
# from django.forms import ModelForm
# from basic.models import *


# форма выбора

VARIANT= [
           
            ("1","1-удельное потребление ниже медианы по группе на 25% с экстремальными коэффициентами С1 или С2."),
            ("2","2-удельное потребление ниже медианы по группе на 25%."),
            ("3","3-удельное потребление ниже медианы по группе с экстремальными коэффициентами С1 или С2.")
        ]
'''

где:
С1 - Hotelling's T-squared < 5% от выборки - показатель аномальности
С2 - Q residuals > 95% от выборки - показатель аномальности          

'''

class MlAnomalyForm(forms.Form):
    month = forms.DateField(label='Месяц для анализа', input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    alpha = forms.IntegerField(label='alpha', widget=forms.NumberInput(attrs={'min': 1, 'max': 100}), initial='5' )
    beta = forms.IntegerField(label='beta', widget=forms.NumberInput(attrs={'min': 1, 'max': 100}), initial='95')   
    variant = forms.ChoiceField(label='Выбрать вариант расчета аномалий', choices=VARIANT, initial="1-2 этажа" )
   
SORTFILTER=[
    ("1","Фактическое потребление - Прогноз < 0"),
    ("2","Фактическое потребление - Прогноз > 0")
]
class ForecastForm(forms.Form):
    month = forms.DateField(label='Месяц для анализа', input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    sortfilter=forms.ChoiceField(label='Сортировать по', choices=SORTFILTER, initial="Фактическое потребление - Прогноз < 0" )
    sample  = forms.IntegerField(label='выборка, %', widget=forms.NumberInput(attrs={'min': 1, 'max': 100}), initial='5' )
