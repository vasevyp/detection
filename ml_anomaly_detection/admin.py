from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ResultMl, MonthResultMl, ForecastData

@admin.register(MonthResultMl)
class MonthResultMlAdmin(ImportExportModelAdmin):
    ''''admin for MonthResultMl'''
    list_display = ['period','odpu_number', 'address2',
                      'current_consumption', 'specific_data','below_median' ]
    save_on_top = True
    search_fields = ('address2',)
    list_filter = ('period',)  

@admin.register(ResultMl)
class ResultMlAdmin(ImportExportModelAdmin):
    ''''admin for ResultMl'''
    list_display = ['period','odpu_number', 'address2',
                      'current_consumption', 'specific_data','below_median' ]
    save_on_top = True
    search_fields = ('address2',)
    list_filter = ('period',)   

@admin.register(ForecastData)
class ForecastDataAdmin(ImportExportModelAdmin):
    ''''admin for ForecastData'''
    list_display = ['period','odpu_number', 'address2', 'specific_data','forecast_index' ]
    save_on_top = True
    search_fields = ('address2',)
    list_filter = ('period',)   