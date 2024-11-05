from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import DoubleData, Apartment, ObjectDataReport


@admin.register(DoubleData)
class DoubleDataAdmin(ImportExportModelAdmin):
    ''''admin total double data for energy'''
    list_display = ['period', 'subunit', 'odpu_number', 'address',
                     'current_date', 'current_consumption' ]
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('period',)
@admin.register(Apartment)
class ApartmentAdmin(ImportExportModelAdmin):
    ''''admin for Apartment'''
    list_display = ['period', 'subunit', 'odpu_number', 'address',
                      'current_consumption', 'specific_data' ]
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('period',)    

@admin.register(ObjectDataReport)
class ObjectDataReportAdmin(ImportExportModelAdmin):
    ''''admin data of heat energy consumer objects'''
    list_display = ['address', 'object_type', 'floors', 'construction_date', 'area']
    save_on_top = True
    search_fields = ('address',)
    list_filter = ('object_type',)    