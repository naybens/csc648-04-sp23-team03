from django.shortcuts import render, redirect
from .forms import PreferenceForm, CategoryForm, ChoiceForm
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_control
from .models import Preference, Category, Choice, History
import json
import requests
import random

yelpKey = 'vndHDucQHzjlz6eixa0ZVhR6NBjq88gTe0yMArhJTs_N3yes77zweuFmge5B9JAtd6U-kreaLJkQzBVZ3cvbImEwK1AEguDXaVs7JCuFHpepONBMyQ0dN0dOAJAjZHYx'


@login_required
def preferences(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        category_form = CategoryForm(request.POST)
        choice_form = ChoiceForm(request.POST)

        if form.is_valid() and category_form.is_valid() and choice_form.is_valid():
            preference = form.save(commit=False)
            preference.user = request.user
            preference.save()
            category = category_form.save(commit=False)
            category.preference = preference
            category.save()
            choice = choice_form.save(commit=False)
            choice.category = category
            choice.save()

            return redirect('searchsummary')
    else:
        form = PreferenceForm()
        category_form = CategoryForm()
        choice_form = ChoiceForm()

    return render(request, 'preferences/preferences.html', {'form': form, 'category_form': category_form, 'choice_form': choice_form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required
def search(request):
    if request.method == 'POST':
        user = request.user
        preference, created = Preference.objects.get_or_create(user=user)

        # Parse JSON data
        data = json.loads(request.body)
        selectedRestaurants = data['selectedRestaurants']
        selectedFoodTypes = data['selectedFoodTypes']
        selectedRadius = data['selectedRadius']
        selectedPrices = data['selectedPrices']
        address = data['address']

        # Combine selectedRestaurants and selectedFoodTypes to create selectedChoices
        selectedChoices = selectedRestaurants + selectedFoodTypes

        # Define the categories and their related choices
        category_data = {
            'Restaurants': selectedRestaurants,
            'FoodTypes': selectedFoodTypes,
            'Radius': [selectedRadius],
            'Price': [selectedPrices]
        }

        # Update Categories and Choices for the given preference
        for category_name, choices_data in category_data.items():
            # Get or create the Category
            category, _ = Category.objects.get_or_create(
                preference=preference, text=category_name)

            # Update the related Choices
            # Remove old choices
            Choice.objects.filter(category=category).delete()
            for choice_text in choices_data:
                Choice.objects.create(category=category, text=str(choice_text))

        # making Yelp API search with preferences:
        url = 'https://api.yelp.com/v3/businesses/search'
        headers = {
            'Authorization': f'Bearer {yelpKey}'
        }
        params = {
            'term': 'food, restaurants',
            'categories': ','.join(selectedChoices),
            'radius': selectedRadius,
            'location': address,
            'price': selectedPrices,
        }

        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)
        if 'error' in data:
            print('error')
            return JsonResponse({'error': 'data error.'})
        else:
            if 'businesses' in data and data['businesses']:
                restaurant = random.choice(data['businesses'])
                print(restaurant['name'], restaurant['location']
                    ['address1'], restaurant['price'])

                # Store the selected restaurant in the session
                request.session['selected_restaurant'] = restaurant

                # Saves the selected restaurant in history
                History.objects.create(
                    user=user,
                    restaurant_text=restaurant['name'],
                    image_url=restaurant['image_url'])
            else:
                return JsonResponse({'error': 'Could not find a restaurant! Please broaden your search.'}, status=400)
        return JsonResponse(restaurant)
