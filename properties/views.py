from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

#cache this for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    qs = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    #return json with top level key as data
    return JsonResponse({"data": list(qs)})

