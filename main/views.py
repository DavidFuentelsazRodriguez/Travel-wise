from django.conf import settings
from django.shortcuts import render
from main.populate import populate_db
from main.whoosh_index import load_schema, duration_in_minutes
from main.forms import SearchByNameOrDescriptionForm, SearchByPriceForm, SearchByDurationForm
from main.search import search_by_name_or_description, search_by_price, search_by_duration

# Create your views here.

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

def load_db(request):
    loaded_cities_msg, loades_activities_msg = populate_db()
    return render(request, 'populate.html', {'loaded_cities':loaded_cities_msg, 'loaded_activities':loades_activities_msg})

def load_schema_data(request):
    loaded_index_msg = load_schema()
    return render(request, 'load_schema.html', {'loaded_index':loaded_index_msg})

def search_by_name_or_description_view(request):
    form = SearchByNameOrDescriptionForm()
    activities = []
    
    if request.method == 'POST':
        form = SearchByNameOrDescriptionForm(request.POST)
        
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            activities = search_by_name_or_description(keywords)
            
    return render(request, 'search_by_name_or_description.html', {'form': form, 'activities':activities});

def search_by_price_view(request):
    form = SearchByPriceForm()
    lower_price = 0
    higher_price = 100
    activities = []
    
    if request.method == 'POST':
        form = SearchByPriceForm(request.POST)
        
        if form.is_valid():
            lower_price = form.cleaned_data['lower_price']
            higher_price = form.cleaned_data['higher_price']
            activities = search_by_price(lower_price,higher_price)
            
    return render(request, 'search_by_price.html', context={'form':form, 'lower_price':lower_price, 'higher_price':higher_price, 'activities':activities})

def search_by_duration_view(request):
    form = SearchByDurationForm()
    hours = 0
    minutes = 0
    activities = []
    
    if request.method == 'POST':
        form = SearchByDurationForm(request.POST)
        
        if form.is_valid():
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']
            if not hours:
                hours = 0
        
            if not minutes:
                minutes = 0
            
            duration_in_minutes = parse_duration(hours, minutes)
            activities = search_by_duration(duration_in_minutes)
            
    return render(request, 'search_by_duration.html', 
                  context={'form':form, 'hours':hours, 'minutes':minutes,'activities':activities})

def parse_duration(hours, minutes):
        return hours * 60 + minutes
