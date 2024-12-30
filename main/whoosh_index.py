import os 

from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD, NUMERIC, BOOLEAN
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh.query import NumericRange
from whoosh import qparser, query
from datetime import datetime
from whoosh.query import DateRange, TermRange

from extract_data import extract_activities
from populate import parse_duration

INDEX_DIR = 'indexdir'

def load_schema():
    activities = extract_activities()
    schema = Schema(name=TEXT(stored=True),
                    description=TEXT(stored=True),
                    price=NUMERIC(float),
                    city=TEXT(stored=True, phrase=False),
                    duration=DATETIME(stored=True),
                    has_badge_excellence=BOOLEAN(stored=True),
                    recommendation_rate=NUMERIC(stored=True, sortable=True))
    
    
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    for activity in activities:
        writer.add_document(name=activity[0], description=activity[7], price=parse_price(activity[1]),
                            city=parse_city(activity[4]), duration=parse_duration(activity[2]), has_badge_excellence=activity[6],
                            recommendation_rate=parse_recommendation_rate(activity[5]))
    writer.commit()
    print('INDICE CREADO',f'Número de eventos almacenados:{ix.reader().doc_count()}')

def parse_price(str_price):
    return float(str_price).split('€')[0].strip()

def parse_city(city):
    return city if city is not None else 'Unknown city'

def parse_recommendation_rate(str_recommendation_rate):
    return int(str_recommendation_rate) if str_recommendation_rate is not None else 0
        

load_schema()