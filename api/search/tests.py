from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Search

class SearchTests(APITestCase):
    def test_create_search(self):
        url = reverse('create_search')
        data = {"text": "example", "file_mask": "*.txt"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("search_id", response.data)

    def test_get_search_results(self):
        search = Search.objects.create(text="example")
        url = reverse('get_search_results', args=[search.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
