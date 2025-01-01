import os 

from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD, NUMERIC, BOOLEAN
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh.query import NumericRange
from whoosh import qparser, query
from datetime import datetime
from whoosh.query import DateRange, TermRange

INDEX_DIR = 'indexdir'

def search_by_name_or_description(words):
    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        query = MultifieldParser(['name','description'], ix.schema).parse(words)
        results = searcher.search(query, limit=None)
        activities = [
            {
                "name": hit.get("name", "N/A"),
                "description": hit.get("description", "N/A"),
                "price": hit.get("price", "N/A"),
                "city": hit.get("city", "N/A"),
                "duration": hit.get("duration", "N/A"),
                "recommendation_rate": hit.get("recommendation_rate", "N/A"),
                "has_badge_excellence": hit.get("has_badge_excellence", False),
            }
            for hit in results
        ]
    return activities

    