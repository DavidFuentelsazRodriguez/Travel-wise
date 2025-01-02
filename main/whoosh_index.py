import os 

from whoosh.fields import Schema, TEXT, NUMERIC, BOOLEAN
from whoosh.index import create_in

from main.populate import populate_db
from main.models import Activity

INDEX_DIR = 'indexdir'

def load_schema():
    activities = list(Activity.objects.all())
    if len(activities) == 0:
        populate_db()
        activities = list(Activity.objects.all())
        
    schema = Schema(name=TEXT(stored=True),
                    description=TEXT(stored=True),
                    price=NUMERIC(float, stored=True),
                    city=TEXT(stored=True, phrase=False),
                    duration=NUMERIC(stored=True, sortable=True),
                    has_badge_excellence=BOOLEAN(stored=True),
                    recommendation_rate=NUMERIC(stored=True, sortable=True))
    
    
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    
    for activity in activities:
        writer.add_document(name=activity.name, description=activity.description, price=activity.price,
                            city=activity.city.name, duration=duration_in_minutes(activity.duration), has_badge_excellence=activity.has_badge_excellence,
                            recommendation_rate=activity.recommendation_rate)
    writer.commit()
    created_index_msg = f'Indice creado exitosamente, se han añadido {ix.reader().doc_count()} actividades'
    return created_index_msg
    
def duration_in_minutes(duration):
    return duration.hour * 60 + duration.minute if duration else 0
