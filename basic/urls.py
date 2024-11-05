from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *
from .views_load import *

urlpatterns = [
    path('', enter_page, name='enter_page'),
    path('main', start_page, name='main'),
    path('contact', contact_page, name='contact'),
    path('energy-data-month', cache_page(60)(EnergyDataListView.as_view()), name='energy_data_month'),
    path('energy-data-month-none', energy_data_none, name='energy_data_month_none'),
    path('energy-data', cache_page(60)(EnergyDataTotalListView.as_view()), name='energy_data_total'),
    path('energy-data-none', EnergyDataTotalNoneListView.as_view(), name='energy_data_total_none'),
    path('energy-data-loading/', energy_data_loading, name='energy_data_loading'), 
    path('energy-data-save', energy_data_save, name='energy_data_save'),
    path('object-data-loading/', object_data_loading, name='object_data_loading'), 
    path('object-data-save', object_data_save, name='object_data_save'),
    path('objects', cache_page(600)(ObjectDataListView.as_view()), name='objects'),
    path('address-data-none', address_data_none, name='address_data_none'),
    path('address-data-none_month', address_data_none_month, name='address_data_none_month'),
]