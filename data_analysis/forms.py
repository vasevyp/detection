from django import forms
# from django.forms import ModelForm
# from basic.models import *


class PeriodForm(forms.Form):    
    first_date=forms.DateField(label='Начало периода', input_formats=['%Y-%m-%d'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    last_date=forms.DateField(label='Конец периода',input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # recalculation_model = forms.ChoiceField(label='Модель пересчета, Avg, Max, среднее', choices=MODEL, initial='Avg' )

class ObjectForm(forms.Form):       
    # object_address = forms.CharField(label='Адрес объекта')
    object_address = forms.CharField()

class ApartmentMonthForm(forms.Form):    
    month_date=forms.DateField(label='Месяц', input_formats=['%Y-%m-%d'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    ) 
    
class HightLowForm(forms.Form):    
    month_date=forms.DateField(label='Месяц', input_formats=['%Y-%m-%d'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    ) 


# форма выбора
FLOOR_LABEL=[
            ("f1","1-2 этажа"),
            ("f2","3-4 этажа"),
            ("f3","5-9 этажей"),
            ("f4","10-12 этажей"),
            ("f5","13 и более этажей")
            ]
YEAR_LABEL= [
            ("y1","до 1958 г"),
            ("y2","1959-1989 гг."),
            ("y3","1990-2000 гг."),
            ("y4","2001-2010 гг."),
            ("y5","2011-2024 гг.")
        ]

class CriteriaSelectionForm(forms.Form):
    month = forms.DateField(label='Месяц для анализа', input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(attrs={'type': 'date'})
    )    
    floors_group = forms.ChoiceField(label='Этажей', choices=FLOOR_LABEL, initial="1-2 этажа" )
    year_group = forms.ChoiceField(label='Этажей', choices=YEAR_LABEL, initial="до 1958 г" )


# class criteria selectionForm(forms.Form):    
#     first_date=forms.DateField(label='Начало периода для перерасчета ', input_formats=['%d/%m/%Y'], 
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )
#     last_date=forms.DateField(label='Конец периода для перерасчета ',input_formats=['%d/%m/%Y'], 
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )
#     recalculation_model = forms.ChoiceField(label='Модель пересчета, Avg, Max, среднее', choices=MODEL, initial='Avg' )

'''Форма для редактирования Заказа'''
# class OrderEditForm(ModelForm):
#     class Meta:
#         model=Order 
#         fields=['order','delivery_date' ]
#         widgets={
#             'order':forms.NumberInput(attrs={'class':'form-control'}),
#             'delivery_date':forms.DateInput(attrs={'type': 'date'})
#         } 