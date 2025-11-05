from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

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

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Cache metrics
    """
    #connection to the redis instance
    redis_conn = get_redis_connection("default")

    #fetch metrics
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    #remove division by 0 possibility
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics

