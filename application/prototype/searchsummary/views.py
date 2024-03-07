from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from preferences.models import Preference, Category, Choice
from preferences.views import yelpKey, search
import json
import requests
import random
from django.shortcuts import get_object_or_404

from preferences.models import History


@login_required
def search_summary(request):
    selected_restaurant = request.session.get('selected_restaurant', None)
    if not selected_restaurant:
        # Redirect the user back to the preferences page if no restaurant is
        # found in the session
        return redirect('preferences')

    if request.method == 'POST' and 'rating' in request.POST:
        user = request.user
        user_rating = request.POST.get('rating')
        # Get Recent History
        latest_history = History.objects.filter(user=user).order_by(
            '-creation_datetime')[0]
        # Set the Rating
        latest_history.user_rating = user_rating
        latest_history.save()
    elif (request.method == 'POST' and 'reroll' in request.POST):
        print("Reroll!")

        user = request.user

    # Get the Latest Preferences from the Database
        latest_preference = get_object_or_404(Preference.objects.filter(
            user=user).order_by('-creation_datetime')[:1])

        restaurant_category = latest_preference.category_set.filter(
            text__icontains="Restaurants")
        foodtypes_category = latest_preference.category_set.filter(
            text__icontains="FoodTypes")
        radius_category = latest_preference.category_set.filter(
            text__icontains="Radius")
        price_category = latest_preference.category_set.filter(
            text__icontains="Price")

        restaurant_choices = Choice.objects.filter(
            category__in=restaurant_category)
        foodtypes_choices = Choice.objects.filter(
            category__in=foodtypes_category)
        radius_choices = Choice.objects.filter(
            category__in=radius_category)
        price_choices = Choice.objects.filter(
            category__in=price_category)

        restaurants = [choice.text for choice in restaurant_choices]
        food_types = [choice.text for choice in foodtypes_choices]
        radii = [choice.text for choice in radius_choices]
        prices = [choice.text for choice in price_choices]

        #     # Then modify it by making another Yelp API call
        # making Yelp API search with preferences:
        url = 'https://api.yelp.com/v3/businesses/search'
        headers = {
            'Authorization': f'Bearer {yelpKey}'
        }
        params = {
            'term': 'food, restaurants',
            'categories': ','.join(restaurants + food_types),
            'radius': ','.join(radii),
            'location': 'SFSU',
            'price': ','.join(prices),
        }

        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)
        if 'error' in data:
            print('error')
            return JsonResponse({'error': 'string'})
        else:
            restaurant = random.choice(data['businesses'])
            print(restaurant['name'], restaurant['location']
                  ['address1'], restaurant['price'])

            recent_history = History.objects.filter(
                user=user).first()

            # Store the selected restaurant in the session
            request.session['selected_restaurant'] = restaurant

            recent_history.restaurant_text = restaurant['name']
            recent_history.image_url = restaurant['image_url']

            recent_history.save()

        selected_restaurant = request.session.get(
            'selected_restaurant', None)
    return render(request, 'searchsummary/searchsummary.html',
                  {'restaurant': selected_restaurant})
