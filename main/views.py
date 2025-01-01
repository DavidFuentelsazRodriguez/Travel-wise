from django.conf import settings
from django.shortcuts import render
from main.populate import populate_db
from main.whoosh_index import load_schema
from main.forms import SearchByNameOrDescriptionForm
from main.search import search_by_name_or_description

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