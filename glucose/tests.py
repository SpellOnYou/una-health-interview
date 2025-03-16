from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now

# Unit test cases for the GlucoseLevel API
class GlucoseLevelAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sample_data = {
            "user_id": "test_user",
            "timestamp": now().isoformat(),
            "value": 100.5
        }

    def test_create_glucose_level(self):
        response = self.client.post('/api/v1/upload/', self.sample_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_glucose_levels(self):
        response = self.client.get('/api/v1/levels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_glucose_levels(self):
        response = self.client.get('/api/v1/export/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')