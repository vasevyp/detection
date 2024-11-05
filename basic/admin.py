"""admin file"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import EnergyData, EnergyDataTotal, AnomalEnergyData, ObjectData, ObjectDataLoad

@admin.register(EnergyData)
class EnergyDataAdmin(ImportExportModelAdmin):
    ''''admin data for energy'''
    list_display = ['period', 'subunit', 'odpu_number', 'address',
                     'current_date', 'current_consumption' ]
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('period',)

@admin.register(EnergyDataTotal)
class EnergyDataTotalAdmin(ImportExportModelAdmin):
    ''''admin total data for energy'''
    list_display = [ 'address','period', 'subunit', 'odpu_number',
                     'current_date', 'current_consumption' ]
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('period',)

@admin.register(AnomalEnergyData)
class AnomalEnergyDataAdmin(ImportExportModelAdmin):
    ''''admin total anomal data for energy'''
    list_display = ['period', 'subunit', 'odpu_number', 'address',
                     'current_date', 'current_consumption' ]
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('period',)    

@admin.register(ObjectData)
class ObjectDataAdmin(ImportExportModelAdmin):
    ''''admin data of heat energy consumer objects'''
    list_display = ['address', 'object_type', 'floors', 'construction_date', 'area']
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('object_type',)

@admin.register(ObjectDataLoad)
class ObjectDataLoadAdmin(ImportExportModelAdmin):
    ''''admin data of heat energy consumer objects'''
    list_display = ['address', 'object_type', 'floors', 'construction_date', 'area']
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('object_type',)    