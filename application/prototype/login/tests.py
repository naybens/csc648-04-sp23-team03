from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse  # Add this import
from rest_framework.authtoken.models import Token

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='unittestuser',
            email='unit_test_user@test.com',
            password='unittestuser'
        )

    def test_login_page_render(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_successful_login(self):
        response = self.client.post('/login/tokenauth', {
            'username': 'unittestuser',
            'password': 'unittestuser',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())
        self.assertTrue('session_key' in response.json())

    def test_invalid_username(self):
        response = self.client.post('/login/tokenauth', {
            'username': 'wrongusername',
            'password': 'unittestuser',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], 'Invalid username or password')

    def test_invalid_password(self):
        response = self.client.post('/login/tokenauth', {
            'username': 'unittestuser',
            'password': 'wrongpassword',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], 'Invalid username or password')
        
    #def test_invalid_request_method(self):
    #    response = self.client.get('/login/tokenauth')
    #    self.assertEqual(response.status_code, 405)  # 405 Method Not Allowed
    #    self.assertEqual(response.content.decode(), 'Invalid request method')

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='unittestuser',
            email='unit_test_user@test.com',
            password='unittestuser'
        )
"""
    def test_successful_login_redirect(self):
        response = self.client.post('/login/tokenauth', {
            'username': 'unittestuser',
            'password': 'unittestuser',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        token = response.json()['token']
        session_key = response.json()['session_key']

        self.client.cookies['sessionid'] = session_key
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Token {token}'

        data = {  # Define the data variable
            'username': 'unittestuser',
            'password': 'unittestuser',
        }

        response = self.client.post(reverse('login'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences/preferences.html')
"""
