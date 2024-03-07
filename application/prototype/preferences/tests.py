from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Preference, Category, Choice, History
import json

class PreferencePageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_preferences_view_logged_in(self):
        # Test case for logged-in user preferences view.
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences/preferences.html')

    def test_search_view_logged_in(self):
        # Test case for logged-in user search.
        self.client.login(username='testuser', password='password')
        preference = Preference.objects.create(user=self.user)
        category1 = Category.objects.create(preference=preference, text='Restaurants')
        category2 = Category.objects.create(preference=preference, text='FoodTypes')
        choice1 = Choice.objects.create(category=category1, text='Chinese')
        choice2 = Choice.objects.create(category=category2, text='Vegetarian')
        
        # Create a new token for the user
        token = Token.objects.create(user=self.user)
        
        headers = {'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        response = self.client.post(reverse('search'), {'selectedRestaurants': ['Chinese'], 'selectedFoodTypes': ['Vegetarian'], 'selectedRadius': '1000', 'selectedPrices': '1,2', 'address': 'San Francisco, CA, USA'}, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')
        self.assertContains(response, 'location')
        self.assertContains(response, 'price')

    def test_preference_model(self):
        # Test case for the Preference model.
        preference = Preference.objects.create(user=self.user)
        self.assertEqual(preference.user, self.user)

    def test_category_model(self):
        # Test case for the Category model.
        preference = Preference.objects.create(user=self.user)
        category = Category.objects.create(preference=preference, text='Restaurants')
        self.assertEqual(category.preference, preference)
        self.assertEqual(category.text, 'Restaurants')

    def test_choice_model(self):
        # Test case for the Choice model.
        preference = Preference.objects.create(user=self.user)
        category = Category.objects.create(preference=preference, text='Restaurants')
        choice = Choice.objects.create(category=category, text='Chinese')
        self.assertEqual(choice.category, category)
        self.assertEqual(choice.text, 'Chinese')

    def test_history_model(self):
        # Test case for the History model.
        history = History.objects.create(user=self.user, restaurant_text='Chinese Restaurant', image_url='https://www.example.com/chinese.jpg')
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.restaurant_text, 'Chinese Restaurant')
        self.assertEqual(history.image_url, 'https://www.example.com/chinese.jpg')

    def test_search_view_logged_in(self):
        # Test case for logged-in user search.
        self.client.login(username='testuser', password='password')
        preference = Preference.objects.create(user=self.user)
        category1 = Category.objects.create(preference=preference, text='Restaurants')
        category2 = Category.objects.create(preference=preference, text='FoodTypes')
        choice1 = Choice.objects.create(category=category1, text='Chinese')
        choice2 = Choice.objects.create(category=category2, text='Vegetarian')

        # Create a new token for the user
        token = Token.objects.create(user=self.user)

        headers = {'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        response = self.client.post(reverse('search'), {'selectedRestaurants': ['Chinese'], 'selectedFoodTypes': ['Vegetarian'], 'selectedRadius': '1000', 'selectedPrices': '1,2', 'address': 'San Francisco, CA, USA'}, content_type='application/json', **headers)

        # Store the response content
        response_content = response.content

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')
        self.assertContains(response, 'location')
        self.assertContains(response, 'price')

         # Store the result in a variable
        result = json.loads(response.content)
        
        # Check if the selected restaurant is saved in the history
        history = History.objects.filter(user=self.user, restaurant_text=result['name']).exists()
        if history:
            print("History found")
            data = json.loads(response_content)
            name = data['name']
            address = ', '.join(data['location']['display_address'])
            price = data['price']
            result_string = f'{name} {address} {price}'
            print(result_string)  # Output: The Sausage Factory 517 Castro St, San Francisco, CA 94114 $$
        self.assertTrue(history)