from datetime import datetime
import sqlite3
import numpy as np
import pandas as pd

from django.shortcuts import render
# from django.db.models import Q 
from django.views.generic import ListView
# from django.core.paginator import Paginator
# from django.db.models import Count, Sum, Avg, Max, Min

from basic.models import EnergyDataTotal, AnomalEnergyData, ObjectData, EnergyData
from .models import DoubleData, Apartment, ObjectDataReport

from .forms import PeriodForm, ObjectForm, ApartmentMonthForm

def in_dev(request):
    """Function showing page in dev."""
    return render(request, 'in_dev.html' )

def service_list(request):
    """Function showing page service_list."""
    return render(request, 'service/service_list.html' )
    
def period_selection(request):
    ''''Выбор аномальных данных по заданному интервалу периодов'''
    form=PeriodForm
    items=''
    item=''
    first_date =''
    last_date=''
    if request.method == "POST":
        first_date = request.POST.get("first_date")
        last_date = request.POST.get("last_date")

        items=AnomalEnergyData.objects.filter(period__range=(first_date, last_date)).order_by('address')
        item=AnomalEnergyData.objects.filter(period__range=(first_date, last_date))
    first_period = AnomalEnergyData.objects.first().period
    last_period = AnomalEnergyData.objects.last().period
    if items:
        first_d = item[0].period
        last_d= item.reverse()[0].period
    else:
        first_d = ''
        last_d= ''

    return render(request, "forms/period_form.html", {'first_period':first_period, 'last_period':last_period, 'items':items,'form':form, 'first_date':first_d, 'last_date':last_d })    

def object_selection(request):
    '''Выбор полных данных по адресу за все периоды'''
    form=ObjectForm
    items=''
    address=''
    select_except =False
    first_period = EnergyDataTotal.objects.first().period
    last_period = EnergyDataTotal.objects.last().period
    if request.method == "POST":
        address = request.POST.get("object_address")

        address=address.strip()

        item = EnergyDataTotal.objects.filter(address=address)
        if item :
            print('OK address', address)
            items = EnergyDataTotal.objects.filter(address=address)
        else:
            select_except='По адресу нет данных о потреблении тепловой энергии'
            print('NO address', address)
            return render(request, "forms/object_form.html", {'select_except':select_except, 'address':address, 'first_period':first_period, 'last_period':last_period})
    objects=ObjectDataReport.objects.all()
    return render(request, "forms/object_form.html", {'first_period':first_period, 'last_period':last_period, 'items':items,'form':form, 'objects':objects, 'select_except': select_except })   


def double_data(request):
    '''Вывод данных по объекта с одинаковым потреблением в разные периоды'''
    print('RUN FUNCTION DOUBLE_DATA')

    items=DoubleData.objects.all().order_by('address', '-current_consumption', '-period')
   
    return render(request, 'data_analysis/double_data.html', {'items':items})


def apartment(request):
    '''abnormally low/high (deviation more than 25%) consumption of the object in a given month compared to similar objects (only for the object types "Apartment building")'''
    period=EnergyData.objects.first().period

    items=Apartment.objects.all()
    # items = EnergyDataTotal.objects.filter(object_type='Многоквартирный дом',  energy_type='ГВС-ИТП').order_by('address', '-period')
    context={
        'items':items,
    }
    return render(request, 'data_analysis/apartment.html', context)


class ObjectDataReportListView(ListView):
    """class for month list data by Objects from report"""
    model= ObjectDataReport
    template_name='data_analysis/object_data_report.html'
    context_object_name = 'items'
    ordering = ['address']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=ObjectDataReport.objects.all()
        ObjectDataReport.objects.order_by('address')
        context['item_count'] = item.count
        return context

class ApartmentListView(ListView):
    """class for month list data by Objects from report"""
    model= Apartment
    template_name='data_analysis/apartment.html'
    context_object_name = 'items'
    ordering = ['address','-period']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=Apartment.objects.all()
        # ObjectDataReport.objects.order_by('address')
        context['item_count'] = item.count
        return context

''' Выбор данных аномально низкого/высокого (отклонение более 25%) потребления объекта в конкретном месяце'''
def period_abnormal_selection(request):
    '''Выбор данных аномально низкого/высокого (отклонение более 25%) потребления объекта в конкретном месяце '''
    form=ApartmentMonthForm
    items = ''
    month_date=''
    date_object=''
    select_except =False  
    if request.method == "POST":
        month_date = request.POST.get("month_date")  
        print(type(month_date)) 
        date_object = datetime.strptime(month_date, "%Y-%m-%d").date()
        if month_date:
            print('OK address', month_date)
            items = Apartment.objects.filter(period=month_date).exclude(index_abnormal= 0).exclude(index_abnormal= None)
            # print(items[0].index_abnormal, type(items[0].index_abnormal), type(items[0].period) )
        else:
            select_except=f'Периода {month_date} нет в данных о потреблении тепловой энергии'  
            print('NO month_date', month_date)
            return render(request, "forms/apartment_abnormal_form.html", {'select_except':select_except})     

    return render(request, "forms/apartment_abnormal_form.html", {'form':form,  'items': items, 'select_except': select_except, 'month_date':date_object, 'items.count': items.count })   


