import sqlite3
import time

from django.views.generic import ListView
from django.core.paginator import Paginator

# from datetime import datetime
from django.shortcuts import render, redirect

import openpyxl
import pandas as pd
import numpy as np

from .models import ResultMl, MonthResultMl, TempAnomalData, ForecastData
from .forms import MlAnomalyForm, ForecastForm


def result_data_loading(request):
    """1.Загрузка ML-результата расчета аномального потребления энергии за месяц из xlsx file with pandas"""
    print("start month_result_data_loading")
    try:
        if request.method == "POST" and request.FILES["myfile"]:
            print("if POST -OK")  # +
            myfile = request.FILES["myfile"]
            print("myfile==", myfile)  # +
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            print("dataframe shape ==\n", df.tail(2), "\ntype data:", type(df))
            conn = sqlite3.connect("db.sqlite3")
            print("conn--", conn)
            df.to_sql("ml_anomaly_detection_monthresultml", conn, if_exists="replace") #if_exists="replace" if_exists="append"
            # таблица для данных append
            # data=EnergyData.objects.all()  #append   replace

            return render(
                request,
                "result_load/result_loading.html",
                {"myfile": myfile, "datas": data},
            )
    except TypeError as identifier:
        print("Exception as identifier=", identifier)
        return render(
            request, "result_load/result_loading.html", {"item_except": identifier}
        )

    return render(request, "result_load/result_loading.html", {})


def result_data_save(request):
    """1-1.Сохранение импортированных из xlsx файла ML-результатов расчета аномалий по потреблению энергии в Базу Данных"""
    start = time.time()
    print("Выполняется Функция month_result_data_save")
   
    items = MonthResultMl.objects.all()
    for item in items:
        try:
            print("Это объект = ", item.odpu_number)
            ResultMl.objects.get_or_create(
                address2=item.address2,
                object_type=item.object_type,
                odpu_number=item.odpu_number,
                energy_type=item.energy_type,
                floors=item.floors,
                construction_date=item.construction_date,
                area=item.area,
                floors_group=item.floors_group,
                construction_group=item.construction_group,
                current_consumption=item.current_consumption,
                specific_data=item.specific_data,
                t_squared=item.t_squared,
                q_residuals=item.q_residuals,
                below_median=item.below_median,
                median_below25=item.median_below25,
                median_above25=item.median_above25,
                period=item.period
            )          
            
        except Exception as e:
            print("Exception as identifier=", e)
            return render(
                request,
                "result_load/result_loading.html",
                {"loading_except": f" ОШИБКА: - {e}"},
            )
 
    print("ResultMlDB created")

    success = "Загрузка и сохранение данных выполнена успешно!"
    record_time = time.time() - start
    print("Время исполнения: ", record_time / 60, "мин.")
    return render(
        request,
        "result_load/result_loading.html",
        context={"message_success": success, "record_time": record_time / 60},
    )


def show_result_month(request):
    items = MonthResultMl.objects.all()
    return render(
        request,
        "result/month_result.html",
        {
            "items": items,
        },
    )


def show_result(request):
    items = ResultMl.objects.all()
   
    return render(
        request,
        "result/result.html",
        {
            "items": items,
           
        },
    )

class ShowResultListView(ListView):
    """class for Objects data"""
    model= ResultMl
    template_name='result/result.html'
    context_object_name = 'items'
    # ordering = ['address22']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=ResultMl.objects.all()
        context['item_count'] = item.count
        return context

def select_mlanomaly_form(request):
    ''''Выбор аномальных данных ML-model по заданному периоду'''
    form=MlAnomalyForm
    items=''
    variant=''
    alpha =''
    beta=''
    month=''
    data_month=''
    if request.method == "POST":
        month = request.POST.get("month")
        alpha = request.POST.get("alpha")
        beta = request.POST.get("beta")
        variant = request.POST.get("variant")
        print(month, alpha, beta, variant)

        data_month=str(month +' 00:00:00')
        print(data_month)
        # 2021-12-01 00:00:00

    items=ResultMl.objects.filter(period=data_month)
    
    df=pd.DataFrame(list(
        items.values(
            "period", "address2","object_type", "odpu_number", "energy_type", "floors","construction_date", "area", "floors_group", "construction_group", "current_consumption", "specific_data",  "t_squared", "q_residuals", "below_median", "median_below25", "median_above25")))
    queryset=[]
    select_variant=''
    if variant == '1':
        print('variant 1')
        select_variant ='удельное потребление ниже медианы по группе на 25% с экстремальными коэффициентами С1 или С2.' 
              
        q1 = np.percentile(df["t_squared"], int(alpha))
        q2 = np.percentile(df["q_residuals"], int(beta))
        print(q1, q2)
        cond1 = df["t_squared"] < q1
        cond2 = df["q_residuals"] > q2
        cond3 = df["below_median"] == True
        cond4 = df["median_below25"] == True

        df = df[(cond1 | cond2) & cond4]
        TempAnomalData.objects.all().delete()
        for index, row in df.iterrows():
            TempAnomalData.objects.create(
            period=row["period"],
            address2=row["address2"],
            object_type=row["object_type"],
            odpu_number=row["odpu_number"],
            energy_type=row["energy_type"],
            floors=row["floors"],
            construction_date=row["construction_date"],
            area=row["area"],
            floors_group=row["floors_group"],
            construction_group=row["construction_group"],         
            current_consumption=row["current_consumption"],                
            specific_data=row["specific_data"],
            t_squared=row["t_squared"],
            q_residuals=row["q_residuals"],
            below_median=row["below_median"],
            median_below25=row["median_below25"],
            median_above25=row["median_above25"],
        )  # Convert DataFrame to Django Model instances and save
            print(index)
        queryset = TempAnomalData.objects.all()       

        df.to_excel("../../books/select_mlanomaly_form1.xlsx", sheet_name="apartment_list")
        print(df)
       

    if variant == '2':
        print('variant 2')
        select_variant = 'удельное потребление ниже медианы по группе на 25%.'
        cond4 = df["median_below25"] == True

        df = df[cond4]
        TempAnomalData.objects.all().delete()
        for index, row in df.iterrows():
            TempAnomalData.objects.create(
            period=row["period"],
            address2=row["address2"],
            object_type=row["object_type"],
            odpu_number=row["odpu_number"],
            energy_type=row["energy_type"],
            floors=row["floors"],
            construction_date=row["construction_date"],
            area=row["area"],
            floors_group=row["floors_group"],
            construction_group=row["construction_group"],         
            current_consumption=row["current_consumption"],                
            specific_data=row["specific_data"],
            t_squared=row["t_squared"],
            q_residuals=row["q_residuals"],
            below_median=row["below_median"],
            median_below25=row["median_below25"],
            median_above25=row["median_above25"],
        )  # Convert DataFrame to Django Model instances and save
            print(index)
        queryset = TempAnomalData.objects.all()

        df.to_excel("../../books/select_mlanomaly_form2.xlsx", sheet_name="apartment_list")
        print(df)
       

    if variant == '3':
        print('variant 3')
        select_variant = 'объекты, у которых удельное потребление ниже медианы по группе с экстремальными коэффициентами С1 или С2.'
        q1 = np.percentile(df["t_squared"], int(alpha))
        q2 = np.percentile(df["q_residuals"], int(beta))
        print(q1, q2)
        cond1 = df["t_squared"] < q1
        cond2 = df["q_residuals"] > q2
        cond3 = df["below_median"] == True
        # cond4 = df["median_below25"] == True

        df = df[(cond1 | cond2) & cond3]
        TempAnomalData.objects.all().delete()
        for index, row in df.iterrows():
            TempAnomalData.objects.create(
            period=row["period"],
            address2=row["address2"],
            object_type=row["object_type"],
            odpu_number=row["odpu_number"],
            energy_type=row["energy_type"],
            floors=row["floors"],
            construction_date=row["construction_date"],
            area=row["area"],
            floors_group=row["floors_group"],
            construction_group=row["construction_group"],         
            current_consumption=row["current_consumption"],                
            specific_data=row["specific_data"],
            t_squared=row["t_squared"],
            q_residuals=row["q_residuals"],
            below_median=row["below_median"],
            median_below25=row["median_below25"],
            median_above25=row["median_above25"],
        )  # Convert DataFrame to Django Model instances and save
            print(index)
        queryset = TempAnomalData.objects.all()
        df.to_excel("../../books/select_mlanomaly_form3.xlsx", sheet_name="apartment_list")
        print(df)
    

    return render(request, "forms/ml_anomaly_form.html", {'period':month, 'variant':select_variant, 'items':queryset,'form':form, 'alpha':alpha, 'beta':beta })    


def forecast_loading(request):
    """1.Загрузка ML-результата расчета прогноза аномального потребления энергии за месяц из xlsx file with pandas"""
    print("start forecast_loading")
    try:
        if request.method == "POST" and request.FILES["myfile"]:
            print("if POST -OK")  # +
            myfile = request.FILES["myfile"]
            print("myfile==", myfile)  # +
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            print("dataframe shape ==\n", df.tail(2), "\ntype data:", type(df))
            conn = sqlite3.connect("db.sqlite3")
            print("conn--", conn)
            df.to_sql("ml_anomaly_detection_forecastdata", conn, if_exists="replace") #if_exists="replace" if_exists="append"
            # таблица для данных append
            # data=EnergyData.objects.all()  #append   replace

            return render(
                request,
                "result_load/forecast_loading.html",
                {"myfile": myfile, "datas": data},
            )
    except TypeError as identifier:
        print("Exception as identifier=", identifier)
        return render(
            request, "result_load/forecast_loading.html", {"item_except": identifier}
        )
    success = "Загрузка и сохранение данных выполнена успешно!"

    return render(request, "result_load/forecast_loading.html", {"message_success": success})


class ShowForecastListView(ListView):
    """class for  Forecast data"""
    model= ForecastData
    template_name='result/forecast.html'
    ordering = ['forecast_deviation']
    context_object_name = 'items'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=ForecastData.objects.all()
        context['item_count'] = item.count
        return context

def select_forecast_form(request):
    ''''Выбор прогнозных данных потребления ML-model по заданному периоду'''
    form=ForecastForm
    items=''
    month=''
    sample=''
    month_sample=''
    data_month=''
    if request.method == "POST":
        month = request.POST.get("month")
        sample  = request.POST.get("sample")
        sortfilter  = request.POST.get("sortfilter")
        sample=int(sample)
        print(month, sample, sortfilter)

        data_month=str(month +' 00:00:00')
        print(data_month)
        # 2021-12-01 00:00:00
        sa= ForecastData.objects.filter(period=data_month).count()/100*sample
        print(sa)
        month_sample = int(sa*100/sample) 
        sortfilter=int(sortfilter)

        if sortfilter == 1:
             items=ForecastData.objects.filter(period=data_month).order_by('forecast_deviation')[:sa]
        if sortfilter == 2:  
            items=ForecastData.objects.filter(period=data_month).order_by('-forecast_deviation')[:sa]
       

    return render(request, "forms/forecast_form.html", {'period':month, 'items':items,'month_sample':month_sample, "sample": sample, 'form':form })    
