import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_wise.settings')

import django
django.setup()


from main.models import City, Activity
from main.extract_data import extract_activities
from datetime import datetime, timedelta


def populate_db():
    clear_db()
    
    default_city, _ = City.objects.get_or_create(name="Unknown City")
    
    activities = extract_activities()
    activities_to_load = []
    
    for activity in activities:
        name = activity['name']
        description = activity['description']
        price = float(activity['price'].split('€')[0].strip())
        city = activity['city']
        duration = parse_duration(activity['duration'])
        has_badge_excellence = activity['badge_of_excellence']
        recommendation_rate = int(activity['recommendation_rate']) if activity['recommendation_rate'] is not None else 0
        
        
        if city and city.strip():  
            city_instance, _ = City.objects.get_or_create(name=city.strip())
        else:  
            print(f"Assigning default city for activity: {name}")
            city_instance = default_city
        
        activities_to_load.append(Activity(name=name, description=description, price=price, 
                                           city=city_instance, duration=duration,
                                           has_badge_excellence=has_badge_excellence, recommendation_rate=recommendation_rate))
    
    Activity.objects.bulk_create(activities_to_load)
    loaded_cities_msg = 'Ciudades añadidas a la BD ' + str(City.objects.all().count())
    loaded_activities_msg = 'Actividades añadidas a la BD ' + str(Activity.objects.all().count())
    return loaded_cities_msg, loaded_activities_msg

def clear_db():
    Activity.objects.all().delete()
    City.objects.all().delete()
    

def parse_duration(duration_str):
    if not duration_str:
        return datetime.strptime("00:00", "%H:%M").time()

    hours = 0
    minutes = 0

    try:
        if "hora" in duration_str:
            hours = int(duration_str.split("hora")[0].strip())

        if "minuto" in duration_str:
            parts = duration_str.split("minuto")[0].strip().split()
            minutes = int(parts[-1]) if len(parts) > 1 else 0
    except ValueError as e:
        print(f"Error parsing duration: {duration_str}. {e}")
        return datetime.strptime("00:00", "%H:%M").time()

    total_time = timedelta(hours=hours, minutes=minutes)
    time_object = (datetime.min + total_time).time()  
    return time_object

    