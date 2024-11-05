from django.urls import path
from .views import result_data_loading,result_data_save, show_result, show_result_month, select_mlanomaly_form, ShowResultListView,  ShowForecastListView, forecast_loading, select_forecast_form



urlpatterns = [
    path('result-loading', result_data_loading, name='result_data_loading'),
    path('result-save', result_data_save, name='result_save'),
    path('result-month', show_result_month, name='result_month'),
    path('select-mlanomaly-form', select_mlanomaly_form, name='select_mlanomaly_form'),
    path('result', ShowResultListView.as_view(), name='result'),
    path('forecast',  ShowForecastListView.as_view(), name='forecast'),
    path('forecast-loading', forecast_loading, name='forecast_loading'),
    path('select-forecast-form', select_forecast_form, name='select_forecast_form'),
]