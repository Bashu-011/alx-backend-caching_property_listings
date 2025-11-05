from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from properties.utils import get_all_properties
from .models import Property

#cache this for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()  #use fn in utils
    return JsonResponse({
        "data": properties,
        "properties": properties
    })

