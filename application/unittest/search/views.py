from django.shortcuts import render

def search(request):
    return render(request, 'search/index.html')

import requests
from django.http import JsonResponse
from django.conf import settings

def yelp_proxy(request):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': f'Bearer {settings.YELP_API_KEY}',
    }
    params = request.GET

    response = requests.get(url, headers=headers, params=params)
    
    return JsonResponse(response.json(), safe=False)
