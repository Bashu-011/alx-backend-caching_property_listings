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
    Get redis cahce metrics
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0 

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.error(f"Redis Cache Metrics: {metrics}")  
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}