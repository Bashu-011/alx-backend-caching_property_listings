from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    All prperties cached by redis for 1 hour
    """
    properties = cache.get('all_properties')  #check cache
    if properties is None:
        print("Nothing in cache - fetching from DB")
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)  #cache for an hour
    else:
        print("Cache hit — loaded from Redis")
    return properties
