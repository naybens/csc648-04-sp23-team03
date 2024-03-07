from django.test import TestCase
from django.urls import reverse

class SearchTemplateTestCase(TestCase):

    def test_search_template_renders_correctly(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/index.html')
