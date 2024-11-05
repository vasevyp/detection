# from datetime import date
# import sqlite3
import logging
import pickle
from typing import Optional, Tuple
import statistics

# from decimal import Decimal

import time
import dataclasses
import numpy as np
import pandas as pd

# from django_pandas.io import read_frame

from django.shortcuts import render, redirect

# from django.db.models import Count
# from django.db.models import Q

from basic.models import EnergyDataTotal, AnomalEnergyData, ObjectData, EnergyData
from .models import DoubleData, Apartment, ObjectDataReport
from .forms import HightLowForm


def double_data_update(request):
    print("RUN FUNCTION DOUBLE_DATA UPDATE")
    DoubleData.objects.all().delete()
    print("DB deleted")

    objects = (
        EnergyDataTotal.objects.all()
        .values(
            "subunit",
            "period",
            "odpu_number",
            "energy_type",
            "address",
            "object_type",
            "current_date",
            "current_consumption",
        )
        .distinct()
    )

    print(objects.count())

    data = pd.DataFrame(objects)
    cond1 = (
        data["current_consumption"].notnull()
        & (data["current_consumption"] != "0.0")
        & (data["current_consumption"] != "0")
    )
    cond2 = (
        data[cond1]
        .groupby(["odpu_number"])["current_consumption"]
        .transform(lambda x: x.duplicated(keep=False))
    )
    equal_values = data[cond1 & cond2].sort_values(["odpu_number", "period"])

    for index, row in equal_values.iterrows():
        DoubleData.objects.get_or_create(
            subunit=row["subunit"],
            odpu_number=row["odpu_number"],
            energy_type=row["energy_type"],
            address=row["address"],
            object_type=row["object_type"],
            current_date=row["current_date"],
            current_consumption=row["current_consumption"],
            period=row["period"],
        )  # Convert DataFrame to Django Model instances and save

    equal_values.to_excel("../../books/update_double_test.xlsx", sheet_name="double")
    print("DB created")
    return redirect("double_data")


def create_object_data_report(request):
    """add addresses to the object database from consumption data"""
    print("Start create_object_report")
    start = time.time()
    
    item_data = list(EnergyDataTotal.objects.all().values("address", "object_type"))
    df = pd.DataFrame(item_data)
    print(df)
    unique_data_address = df.drop_duplicates(subset=['address'])
    unique_data_address.to_excel(
        "../../books/unique_data_address31.xlsx", sheet_name="obj_list"
    )
    unique_data_address = unique_data_address.assign(
        floors=None, construction_date=None, area=None
    )
    unique_data_address['construction_date']=unique_data_address["construction_date"].astype('datetime64[ns]')
    unique_data_address['area']=unique_data_address["area"].astype('float64')
    print('unique==',unique_data_address)
    object_data = list(
        ObjectData.objects.all().values(
            "address", "object_type", "floors", "construction_date", "area"
        )
    )
    object_data_df = pd.DataFrame(object_data)
    print(object_data_df)
    object_data_df=object_data_df.drop_duplicates()
    print(object_data_df)
    object_data_df['construction_date'] = object_data_df['construction_date'].astype('datetime64[ns]')
    object_data_df['area'] = object_data_df['area'].astype('float64')
    objects_unique = pd.merge(
        object_data_df, unique_data_address, how="outer"
    ).drop_duplicates("address")
    print("objects_unique = \n", (objects_unique))
    print("objects_unique type = ", type(objects_unique))
    # objects_unique=objects_unique[objects_unique.isnull()]=''
    objects_unique.to_excel(
        "../../books/objects_unique_test31.xlsx", sheet_name="full_list"
    )
    ObjectDataReport.objects.all().delete()
    for index, row in objects_unique.iterrows():
        ObjectDataReport.objects.get_or_create(
            address = row['address'],
            object_type = row['object_type'],
            floors = row['floors'],
            construction_date = row['construction_date'],
            area = row['area']

        ) # Convert DataFrame to Django Model instances and save
        print(index)

    # print("df==\n", df)
    # print('1 unique_data_address==\n', unique_data_address)
    print("OBJECTS==\n", objects_unique)
    record_time = time.time() - start
    print("TIME=",record_time / 60, "minute")
    print("Finish create_object_report")

    return redirect("objects_report")


def create_apartment_list(request):
    """Recalculation of the database on heat energy consumption in apartment buildings"""
    start = time.time()
    print("RUN create_apartment_list")
    item_data = list(EnergyDataTotal.objects.all().values("address", "object_type"))
    df = pd.DataFrame(item_data)
   
    unique_data_address = df.drop_duplicates()
    unique_data_address.to_excel(
        "../../books/31unique_data_address.xlsx", sheet_name="obj_list"
    )
    unique_data_address = unique_data_address.assign(
        floors=None, construction_date=None, area=None
    )
    unique_data_address['construction_date'] = unique_data_address['construction_date'].astype('datetime64[ns]')
    object_data = list(
        ObjectDataReport.objects.all().values(
            "address", "object_type", "floors", "construction_date", "area"
        )
    )
    object_data_df = pd.DataFrame(object_data)
    object_data_df['construction_date'] = object_data_df['construction_date'].astype('datetime64[ns]')
   
    df1 = pd.merge(object_data_df, unique_data_address, how="outer").drop_duplicates(
        "address"
    )
    df1 = df1.loc[df1["object_type"] == "Многоквартирный дом"]
    df1.to_excel("../../books/31df1_test.xlsx", sheet_name="df1_list")

    item_data = EnergyDataTotal.objects.filter(
        object_type="Многоквартирный дом", energy_type="ГВС-ИТП"
    ).values(
        "subunit",
        "odpu_number",
        "energy_type",
        "address",
        "object_type",
        "current_consumption",
        "period",
    )

   
    df2 = pd.DataFrame(list(item_data))
    df2 = df2.assign(floors="", construction_date="", area="", specific_data=0)

    df2["floors"] = df2["address"].map(df1.set_index("address")["floors"])
    df2["construction_date"] = df2["address"].map(
        df1.set_index("address")["construction_date"]
    )
    df2["area"] = df2["address"].map(df1.set_index("address")["area"])

    df2[["current_consumption", "area"]] = df2[["current_consumption", "area"]].astype(
        float
    )

    df2.loc[df2["area"] > 0, "specific_data"] = df2["current_consumption"] / df2["area"]

    # df2[['period', 'construction_date']] = df2[['period', 'construction_date']].astype(str)

    df2.to_excel(
        "../../books/27total-Apartment_df_test.xlsx", sheet_name="apartment_list"
    )
    Apartment.objects.all().delete()
    for index, row in df2.iterrows():
        Apartment.objects.create(
            subunit=row["subunit"],
            odpu_number=row["odpu_number"],
            energy_type=row["energy_type"],
            address=row["address"],
            object_type=row["object_type"],
            current_consumption=row["current_consumption"],
            period=row["period"],
            floors=row["floors"],
            construction_date=row["construction_date"],
            area=row["area"],
            specific_data=row["specific_data"],
        )  # Convert DataFrame to Django Model instances and save
        print(index)
    item = Apartment.objects.all()
    for i in item:
        if i.floors is None or i.floors == "nan" or i.floors == 0 or i.floors == '':
            i.floors = 0
        if (
            i.construction_date is None
            or i.construction_date == "nan"
            or i.construction_date == 0
            or i.construction_date == 'NaT'
        ):
            i.construction_date = 3000
        else:
            i.construction_date = i.construction_date[:4]
        i.save()
        print(i.odpu_number)

    print("Apartment DB created = OK")

    record_time = time.time() - start
    print("TIME=", record_time / 60, "minute")
    print("Finish create_apartment_list")
    return redirect("apartment")


def print_apartment(request):
    """Print apartment buildings"""
    start = time.time()
    print("RUN print_apartment")
    a_data = list(
        Apartment.objects.all().values(
            "period",
            "subunit",
            "odpu_number",
            "energy_type",
            "address",
            "object_type",
            "floors",
            "construction_date",
            "current_consumption",
            "area",
            "specific_data",
            "object_group",
            "median_value_s",
            "index_abnormal",
            "median_value_s_deviation",
        )
    )
    a_data_df = pd.DataFrame(a_data)
    a_data_df.to_excel("../../books/Apartment_test.xlsx", sheet_name="apartment_list")

    record_time = time.time() - start
    print("TIME=", record_time / 60, "minute")
    return redirect("apartment")


# аномально низкое/высокое (отклонение более 25%) потребление объекта в конкретном месяце
#  по сравнению с аналогичными объектами (только для типов объекта «Многоквартирный дом»)


def apartment_object_group(request):
    start = time.time()
    print("RUN apartment_object_group")

    items = Apartment.objects.order_by("construction_date", "floors")
    for i in items:
        # bloc 11-15
        if int(i.construction_date) < 1959 and int(i.floors) >= 1:
            i.object_group = 11  # "до 1958 г", "1-2 этажа"
        if int(i.construction_date) < 1959 and int(i.floors) > 2:
            i.object_group = 12  # "до 1958 г", "3-4 этажа"
        if int(i.construction_date) < 1959 and int(i.floors) > 4:
            i.object_group = 13  # "до 1958 г",  "5-9 этажей",
        if int(i.construction_date) < 1959 and int(i.floors) > 9:
            i.object_group = 14  # "до 1958 г",  "10-12 этажей",
        if int(i.construction_date) < 1959 and int(i.floors) > 12:
            i.object_group = 15  # "до 1958 г", "13 и более этажей",
        # bloc 21-25
        if int(i.construction_date) > 1958 and int(i.floors) >= 1:
            i.object_group = 21  # "1959-1989 гг.", "1-2 этажа"
        if int(i.construction_date) > 1958 and int(i.floors) > 2:
            i.object_group = 22  # "1959-1989 гг.", "3-4 этажа",
        if int(i.construction_date) > 1958 and int(i.floors) > 4:
            i.object_group = 23  # "1959-1989 гг.",  "5-9 этажей",
        if int(i.construction_date) > 1958 and int(i.floors) > 9:
            i.object_group = 24  # "1959-1989 гг.", "10-12 этажей",
        if int(i.construction_date) > 1958 and int(i.floors) > 12:
            i.object_group = 25  # "1959-1989 гг.",  "13 и более этажей",
        # bloc 31-35
        if int(i.construction_date) > 1989 and int(i.floors) >= 1:
            i.object_group = 31  # "1990-2000 гг.", "1-2 этажа"
        if int(i.construction_date) > 1989 and int(i.floors) > 2:
            i.object_group = 32  # "1990-2000 гг.", "3-4 этажа",
        if int(i.construction_date) > 1989 and int(i.floors) > 4:
            i.object_group = 33  # "1990-2000 гг.",  "5-9 этажей",
        if int(i.construction_date) > 1989 and int(i.floors) > 9:
            i.object_group = 34  # "1990-2000 гг.", "10-12 этажей",
        if int(i.construction_date) > 1989 and int(i.floors) > 12:
            i.object_group = 35  # "1990-2000 гг.",  "13 и более этажей",
        # bloc 41-45
        if int(i.construction_date) > 2000 and int(i.floors) >= 1:
            i.object_group = 41  # "2001-2010 гг.", "1-2 этажа"
        if int(i.construction_date) > 2000 and int(i.floors) > 2:
            i.object_group = 42  # "2001-2010 гг.", "3-4 этажа",
        if int(i.construction_date) > 2000 and int(i.floors) > 4:
            i.object_group = 43  # "2001-2010 гг.",  "5-9 этажей",
        if int(i.construction_date) > 2000 and int(i.floors) > 9:
            i.object_group = 44  # "2001-2010 гг.", "10-12 этажей",
        if int(i.construction_date) > 2000 and int(i.floors) > 12:
            i.object_group = 45  # "2001-2010 гг.",  "13 и более этажей"
        # bloc 51-55
        if (
            int(i.construction_date) > 2010
            and int(i.construction_date) < 2025
            and int(i.floors) >= 1
        ):
            i.object_group = 51  #  "2011-2024 гг.", "1-2 этажа"
        if (
            int(i.construction_date) > 2010
            and int(i.construction_date) < 2025
            and int(i.floors) > 2
        ):
            i.object_group = 52  #  "2011-2024 гг.","3-4 этажа",
        if (
            int(i.construction_date) > 2010
            and int(i.construction_date) < 2025
            and int(i.floors) > 4
        ):
            i.object_group = 53  #  "2011-2024 гг.",  "5-9 этажей",
        if (
            int(i.construction_date) > 2010
            and int(i.construction_date) < 2025
            and int(i.floors) > 9
        ):
            i.object_group = 54  #  "2011-2024 гг.", "10-12 этажей",
        if (
            int(i.construction_date) > 2010
            and int(i.construction_date) < 2025
            and int(i.floors) > 12
        ):
            i.object_group = 55  #  "2011-2024 гг.", "13 и более этажей",
        if int(i.construction_date) == 3000 and int(i.floors) == 0:
            i.object_group = 0
        i.save()
        print(i.odpu_number)

    record_time = time.time() - start
    print("TIME=", record_time / 60, "minute")

    return redirect("apartment")

def hight_low_consumption(request):
    start = time.time()
    print("RUN apartment_object_group")
    form = HightLowForm
    period=''
  
    if request.method == "POST":
        month_date = request.POST.get("month_date")
        print(type(month_date), month_date)
        period = month_date
        group_list = sorted(
            list(
                set(
                    Apartment.objects.order_by("object_group").values_list(
                        "object_group"
                    )
                )
            )
        )

        for j in group_list:
            item = (
                Apartment.objects.filter(object_group=j[0], period=period)
                .exclude(current_consumption=None)
                .exclude(current_consumption="0.0")
                .exclude(current_consumption=0)
                .exclude(specific_data=None)
                .exclude(specific_data="0.0")
                .exclude(specific_data=0)
            )
            for i in item:
                values_specific = list(
                    Apartment.objects.filter(object_group=j[0], period=period)
                    .values_list("specific_data", flat=True)
                    .order_by("specific_data")
                    .exclude(specific_data=None)
                    .exclude(specific_data="0.0")
                    .exclude(specific_data=0)
                )
                ints_s = [float(x) for x in values_specific]
                ints_s.sort()
                median_specific = statistics.median(ints_s)
                i.median_value_s = median_specific
                if (float(i.specific_data) - float(median_specific * 0.75)) * float(
                    i.area
                ) < 0:
                    i.index_abnormal = -1
                    i.median_value_s_deviation = (
                        float(median_specific)
                        * float(i.area)
                        / float(i.current_consumption)
                    )
                elif (float(i.specific_data) - float(median_specific * 1.25)) * float(
                    i.area
                ) > 0:
                    i.index_abnormal = 1
                    i.median_value_s_deviation = (
                        float(median_specific)
                        * float(i.area)
                        / float(i.current_consumption)
                    )
                else:
                    i.index_abnormal = 0
                    i.median_value_s_deviation = (
                        float(median_specific)
                        * float(i.area)
                        / float(i.current_consumption)
                    )

                print(j, i.odpu_number, i.index_abnormal, i.median_value_s_deviation)

                i.save()

        record_time = time.time() - start
        print("TIME=", record_time / 60, "minute")
        print(period, 'OK')

        return redirect("apartment")
   
    return render(request, "forms/month_date_form.html", {"form": form})
