from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest.mock import patch
from preferences.models import History, Preference, Choice, Category
import json
from django.test import RequestFactory
from unittest import mock


class SearchSummaryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.preference = Preference.objects.create(user=self.user)
        self.category1 = Category.objects.create(
            preference=self.preference, text='Restaurants')
        self.category2 = Category.objects.create(
            preference=self.preference, text='FoodTypes')
        self.category3 = Category.objects.create(
            preference=self.preference, text='Radius')
        self.category4 = Category.objects.create(
            preference=self.preference, text='Price')
        self.choice1 = Choice.objects.create(
            category=self.category1, text='Pizza')
        self.choice2 = Choice.objects.create(
            category=self.category2, text='Italian')
        self.choice3 = Choice.objects.create(
            category=self.category3, text='5000')
        self.choice4 = Choice.objects.create(
            category=self.category4, text='$$')
        self.history = History.objects.create(
            user=self.user, restaurant_text='Test Restaurant',
            image_url='http://test.com')
        self.headers = {
            'Authorization': 'Bearer testtoken'
        }

    def test_search_summary_success(self):
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['selected_restaurant'] = 'Test Restaurant'
        session.save()
        url = reverse('search_summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchsummary/searchsummary.html')
        self.assertEqual(response.context['restaurant'], 'Test Restaurant')

    def test_search_summary_redirect_if_no_restaurant(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('search_summary')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('preferences'))

    # TODO: Correctly test for api
    # @patch('requests.get')
    # def test_search_summary_yelp_api_success(self, mock_get):
    #     mock_data = {'businesses': [{'name': 'Test Restaurant', 'location': {
    #         'address1': '123 Test St'}, 'price': '$$'}]}
    #     mock_response = mock_get.return_value
    #     mock_response.status_code = 200
    #     mock_response.text = json.dumps(mock_data)
    #     self.client.login(username='testuser', password='testpass')
    #     url = reverse('search_summary')
    #     response = self.client.post(
    #         url, data={'rating': 5},
        # HTTP_AUTHORIZATION=self.headers['Authorization'])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context['restaurant'], 'Test Restaurant')
    #     history = History.objects.filter(user=self.user).last()
    #     self.assertEqual(history.restaurant_text, 'Test Restaurant')
    #     self.assertEqual(history.image_url, '')
    #     self.assertEqual(history.user_rating, 5)

    # Reroll tests:
    # Comment out if we don't need to perform API calls for Reroll
    @patch('requests.get')
    def test_search_summary_yelp_api_failure(self, mock_get):
        mock_data = {'error': 'invalid_request'}
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.text = json.dumps(mock_data)
        self.client.login(username='testuser', password='testpass')

    def test_history_when_user_rate_five(self):
        self.client.login(username='testuser', password='testpass')
        self.session = self.client.session
        self.session.save()
        self.session['selected_restaurant'] = 'Test Restaurant'
        self.session.save()
        # Create a history
        new_history = History(user=self.user,
                              image_url='www.test.com',
                              restaurant_text='Test Restaurant',
                              user_rating=1)
        new_history.save()

        # Simulate a POST request with a valid rating
        response = self.client.post(reverse('search_summary'), {'rating': '5'})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the selected_restaurant key is set in the session
        self.assertIsNotNone(self.session.get('selected_restaurant'))
        self.assertEqual(History.objects.last().user_rating, 5)


class SearchSummaryBranchCoverageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.session = self.client.session
        self.session.save()

    # User enters to search summary but selected_restaurant is empty
    # Expect to redirect to preferences
    def test_search_summary_no_selected_restaurant(self):
        response = self.client.get(reverse('search_summary'))
        self.assertRedirects(response, reverse('preferences'))
