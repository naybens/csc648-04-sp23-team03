from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from preferences.models import History
from datetime import datetime, timedelta
from django.utils import timezone

class TestSearchHistoryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.history1 = History.objects.create(
            user=self.user,
            restaurant_text='Test Restaurant 1',
            image_url='https://example.com/image1.jpg',
            creation_datetime=timezone.now(),
            user_rating=5
        )
        self.history2 = History.objects.create(
            user=self.user,
            restaurant_text='Test Restaurant 2',
            image_url='https://example.com/image2.jpg',
            creation_datetime=timezone.now() - timedelta(days=1),
            user_rating=3
        )
        self.url = reverse('render_search_history')
        self.client.login(username='testuser', password='testpass')

    def test_render_search_history_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchhistory/latest_history.html')

    def test_render_search_history_view_with_latest_history(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.history1.restaurant_text)
        self.assertContains(response, self.history2.restaurant_text)

    def test_render_search_history_view_with_no_history(self):
        History.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'No history! Sad meow sounds...')

    # def test_render_search_history_view_redirect_if_not_logged_in(self):
    #     self.client.logout()
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, '/accounts/login/?next=' + self.url)