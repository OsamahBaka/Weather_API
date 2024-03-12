from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class WeatherByCityViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_success_response(self):
        # Test success response when city exists
        response = self.client.get('/weather/Jeddah/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_response(self):
        # Test failure response when city parameter is not provided
        response = self.client.get('/weather/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_fail_response2(self):
        # Test failure response when the API request returns an error
        response = self.client.get('/weather/NonexistentCity/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WeatherBulkViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_success_response(self):
        # Test success response when providing valid city list
        data = {"cities": ["Jeddah", "Makkah", "Riyadh"]}
        response = self.client.post('/weather/bulk/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_response(self):
        # Test failure response when not providing city list
        response = self.client.post('/weather/bulk/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WeatherStatisticsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_success_response(self):
        # Test success response when weather data exists
        response = self.client.get('/weather/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
