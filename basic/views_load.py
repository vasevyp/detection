import sqlite3
import time
from datetime import datetime
import re
import openpyxl
import pandas as pd
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Count, Sum, F
from django.core.exceptions import ValidationError 

from data_analysis.models import DoubleData
from .models import EnergyData, EnergyDataTotal, AnomalEnergyData, ObjectData, ObjectDataLoad

def energy_data_loading(request):
    '''1.Загрузка данных за месяц по потреблению энергии из xlsx file with pandas'''
    print('start energy_data_loading')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            print('if POST -OK')#+
            myfile = request.FILES['myfile']
            print('myfile==',myfile)#+
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            print('dataframe shape ==\n',df.tail(2),'\ntype data:',type(df))            
            conn = sqlite3.connect('db.sqlite3')
            print('conn--',conn)
            df.to_sql('basic_energydata',
                                conn, if_exists='replace') 
             #таблица для данных
            data=EnergyData.objects.all()  #append   replace    

            return render(request, 'loading/energy_data_loading.html', 
                          {'myfile': myfile, 'datas':data}
                          )
    except TypeError as identifier:
        print('Exception as identifier=', identifier)
        return render(request, 'loading/energy_data_loading.html', {'item_except': identifier})

    return render(request, 'loading/energy_data_loading.html', {})





def energy_data_save(request):
    '''1-1.Сохранение импортированных из xlsx файла данных по потреблению энергии в Базу Данных'''
    start = time.time() 
    print('Выполняется Функция energy_data_save')
    EnergyData.objects.filter(energy_type='ГВС (централ)').delete()
    items = EnergyData.objects.all()
    for item in items:
        try:
            print('Это объект = ', item.odpu_number)
            EnergyDataTotal.objects.get_or_create(
                period=item.period,
                subunit=item.subunit,
                odpu_number=item.odpu_number,
                energy_type=item.energy_type,
                address=item.address,
                object_type=item.object_type,
                current_date=item.current_date,
                current_consumption=item.current_consumption,
                generated_by=item.generated_by,
                created_date=item.created_date
                 )
        except Exception as e:
            print('Exception as identifier=', e)
            return render(request, 'loading/energy_data_loading.html', {'loading_except': f' ОШИБКА: - {e}'})
    items_n=EnergyData.objects.filter(current_consumption='').distinct() | EnergyData.objects.filter(current_consumption='0.0').distinct() | EnergyData.objects.filter(current_consumption='0').distinct()| EnergyData.objects.filter(current_consumption=None).distinct()
    for item in items_n:
        try:
            AnomalEnergyData.objects.get_or_create(
                    period=item.period,
                    subunit=item.subunit,
                    odpu_number=item.odpu_number,
                    energy_type=item.energy_type,
                    address=item.address,
                    object_type=item.object_type,
                    current_date=item.current_date,
                    current_consumption=item.current_consumption,
                    generated_by=item.generated_by,
                    created_date=item.created_date
                    )
            print('Anomaly = ', item.odpu_number)
        except Exception as e:
            print('Exception as identifier=', e)
            return render(request, 'loading/energy_data_loading.html', {'loading_except': f' ОШИБКА: - {e}'})    
    #double data
    print('Create DOUBLE_DATA model')
    DoubleData.objects.all().delete()
    print('DoubleDB deleted')
   
    objects = EnergyDataTotal.objects.all().values('subunit','period','odpu_number', 'energy_type', 'address', 'object_type', 'current_date', 'current_consumption').distinct()
    data=pd.DataFrame(objects)
    cond1 = (data["current_consumption"].notnull() & (data["current_consumption"] != '0.0') & (data["current_consumption"] != '0'))
    cond2 = (
        data[cond1]
        .groupby(["odpu_number"])["current_consumption"]
        .transform(lambda x: x.duplicated(keep=False))
    )
    equal_values = (
        data[cond1 & cond2]
        .sort_values(["odpu_number", "period"])        
    )
    # Create Duble Data 
    for index, row in equal_values.iterrows():
        DoubleData.objects.get_or_create(
        subunit  = row['subunit'],
        odpu_number = row['odpu_number'],
        energy_type = row['energy_type'],
        address = row['address'],
        object_type = row['object_type'],
        current_date  = row['current_date'],
        current_consumption = row['current_consumption'],
        period = row['period']
        ) # Convert DataFrame to Django Model instances and save
    
    equal_values.to_excel('../double_test.xlsx', sheet_name="double")
    print('DoubleDB created')
    
    success = 'Загрузка и сохранение данных выполнена успешно!'
    record_time=time.time()-start
    print(record_time)
    return render(request, 'loading/energy_data_loading.html', context={'message_success': success, 'record_time':record_time/60})


def object_data_loading(request):
    '''1.Загрузка данных по объектам из xlsx file with pandas'''
    print('start energy_data_loading')
    # data=ObjectData.objects.all().delete()
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            print('if POST -OK')#+
            myfile = request.FILES['myfile']
            print('myfile==',myfile)#+
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            print('dataframe shape ==\n',df.tail(2),'\ntype data:',type(df))            
            conn = sqlite3.connect('db.sqlite3')
            print('conn--',conn)
            df.to_sql('basic_objectdataload',
                                conn, if_exists='replace') 
             #таблица для данных
            data=ObjectData.objects.all()  #append   replace  
            

            return render(request, 'loading/object_data_loading.html', 
                          {'myfile': myfile, 'datas':data}
                          )
    except TypeError as identifier:
        print('Exception as identifier=', identifier)
        return render(request, 'loading/object_data_loading.html', {'item_except': identifier})

    return render(request, 'loading/object_data_loading.html', {})

def object_data_save(request):
    '''1-1.Сохранение импортированных из xlsx файла данных по объектам в Базу Данных'''
    start = time.time() 
    print('Выполняется Функция object_data_save')
    #function data
    object_loads = ObjectDataLoad.objects.all()

    for item in object_loads:
        try:
            if bool(re.search('[а-яА-Я]', str(item.construction_date))):
                item.construction_date=item.construction_date[:10]
            # else:
            #     item.construction_date = datetime.strptime(item.construction_date, '%d.%m.%Y' )#date format               

                print(item.address,'==', item.construction_date,type(item.construction_date))
                # item.construction_date = item.construction_date.strftime('%Y-%m-%d') #str format
                
                if bool(re.search('[а-яА-Я]', str(item.construction_date))):
                    item.construction_date=''
                    print(item.address,'==', item.construction_date, type(item.construction_date))       
            # item.save()
    
            ObjectData.objects.get_or_create(
                address=item.address,
                object_type=item.object_type,
                floors=item.floors,
                construction_date=item.construction_date,
                area=item.area,
                 )
            print(item.address,'==', item.area) 
        except Exception as e:
            print('Exception as identifier=', e)
            return render(request, 'loading/energy_data_loading.html', {'loading_except': f' ОШИБКА: - {e}'})

    print('ObjectDB created')
    
    success = 'Загрузка и сохранение данных выполнена успешно!'
    record_time=time.time()-start
    print('Время исполнения: ',record_time/60, 'мин.')
    return render(request, 'loading/object_data_loading.html', context={'message_success': success, 'record_time':record_time/60})


