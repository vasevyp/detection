from django.urls import path

from .views import *
from .service import double_data_update, create_apartment_list, create_object_data_report, print_apartment, hight_low_consumption, apartment_object_group


urlpatterns = [
    path('in-dev', in_dev, name='in_dev'),
    path('period-selection', period_selection, name='period_selection'),
    path('object-selection', object_selection, name='object_selection'),
    path('double-data', double_data, name='double_data'),
    path('double-data-update', double_data_update, name='double_data_update'),
    path('apartment-list', ApartmentListView.as_view(), name='apartment'),
    path('create-apartment-list', create_apartment_list, name='create_apartment_list'),
    path('add-address', create_object_data_report, name='add_address'),
    path('objects-report', ObjectDataReportListView.as_view(), name='objects_report'),
    path('print-apartment', print_apartment, name='print_apartment'),
    path('service-list',service_list, name='service_list'),
    path('hight-low-consumption', hight_low_consumption, name ='hight_low_consumption'),
    path('apartment-object-group', apartment_object_group, name='apartment_object_group'),
    path('period-abnormal-selection', period_abnormal_selection, name='period_abnormal_selection'),
    
]