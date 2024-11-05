"""Module providing the function of working with data."""
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, Max, Min


from .models import EnergyData, EnergyDataTotal, ObjectDataLoad, ObjectData, AnomalEnergyData
from data_analysis.models import ObjectDataReport

# Create your views here.
def enter_page(request):
    return render(request, 'start/enter_page.html')
def start_page(request):
    """Function showing start page."""
    return render(request, 'start/start_page.html')

def tasks(request):
    """Function showing page in dev."""
    return render(request, 'start/tasks.html' )

def contact_page(request):
    """Function showing start page."""
    return render(request, 'start/contact_page.html')

# month data
class EnergyDataListView(ListView):
    """class for month list energy data"""
    model= EnergyData
    template_name='basic/energy_data.html'
    context_object_name = 'items'
    ordering = ['address']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=EnergyData.objects.all()
        context['item_count'] = item.count
        context['item_period'] = item[0].period
        context['item_generated_by'] = item[0].generated_by
        context['item_created_date'] = item[0].created_date
        return context

address_none_month=set(ObjectDataReport.objects.values_list('address', flat=True).distinct())-set(EnergyData.objects.
                                                                                          values_list('address', flat=True).distinct())
def energy_data_none(requist):
    'Position without data'
    items=EnergyData.objects.filter(current_consumption='').order_by('address') | EnergyData.objects.filter(current_consumption=0).order_by('address')| EnergyData.objects.filter(current_consumption=None).order_by('address')
   
    context={
        'items':items,
        'item_period':items[0].period,
        'item_generated_by':items[0].generated_by,
        'item_created_date':items[0].created_date,
        'address_none':len(address_none_month), 
    }
    return render(requist, 'anomaly/energy_data_none.html', context)


# total data
class EnergyDataTotalListView(ListView):
    """class for list total energy data"""
    model= EnergyDataTotal
    template_name='basic/energy_data_total.html'
    context_object_name = 'items'
    ordering = ['address']
    paginate_by = 50

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=EnergyDataTotal.objects.all()
        context['item_count'] = item.count
        context['item_period_l'] = EnergyDataTotal.objects.first().period
        context['item_period_f'] = EnergyDataTotal.objects.last().period

        return context
#Get addresses that are not included in the total consumption report
address_none=set(ObjectDataReport.objects.values_list('address', flat=True).distinct())-set(EnergyDataTotal.objects.
                                                                                          values_list('address', flat=True).distinct())

def energy_data_total_none(request):
    'Address position without data'
    items_n=EnergyDataTotal.objects.filter(current_consumption='').order_by('address') | EnergyDataTotal.objects.filter(current_consumption='0.0').order_by('address') | EnergyDataTotal.objects.filter(current_consumption='0').order_by('address')| EnergyDataTotal.objects.filter(current_consumption=None).order_by('address')
    # items_n=AnomalEnergyData.objects.all()
    paginator = Paginator(items_n, 5)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context={
        'items':items_n,
        'item_period_l':EnergyDataTotal.objects.first().period,
        'item_period_f':EnergyDataTotal.objects.last().period,
        'address_none':len(address_none),
        'page_obj':page_obj, 
    }
    

    return render(request, 'anomaly/energy_data_total_none.html', context)

class EnergyDataTotalNoneListView(ListView):
    """class for list total anomaly energy data"""
    model= AnomalEnergyData
    template_name='anomaly/energy_data_total_none.html'
    context_object_name = 'items'
    ordering = ['address']
    paginate_by = 50

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item0=AnomalEnergyData.objects.all()
        context['item_count'] = item0.count
        context['item_period_l'] = AnomalEnergyData.objects.first().period
        context['item_period_f'] = AnomalEnergyData.objects.last().period
        context['address_none']=len(address_none)

        return context


def address_data_none(request):
    '''Show addresses that are not included in the consumption report'''
    show_address_none=sorted(address_none)
    return render(request, 'anomaly/show_address_none.html', {'items':show_address_none, 'items_count':len(address_none)})

def address_data_none_month(request):
    '''Show addresses that are not included in the month consumption report'''
    show_address_none=sorted(address_none_month)
    return render(request, 'anomaly/show_address_none_month.html', {'items':show_address_none, 'items_count':len(address_none_month)})


class ObjectDataListView(ListView):
    """class for Objects data"""
    model= ObjectDataLoad
    template_name='basic/object_data.html'
    context_object_name = 'items'
    ordering = ['address']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet count 
        item=ObjectDataLoad.objects.all()
        ObjectDataLoad.objects.order_by('address')
        context['item_count'] = item.count
        return context
