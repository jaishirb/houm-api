from rest_framework import status
from rest_framework.test import APITestCase

from apps.houmers.factories import PropertyFactory
from apps.houmers.models import Houmer


class HoumTestCase(APITestCase):
    """
    setting up the superuser for the tests and the login for rest-auth
    """
    def setUp(self):
        self.superuser = Houmer.objects.create_superuser('admin', 'admin@admin.com', '123456')
        self.client.login(username='admin', password='123456')

    def test_create_properties_ok(self):
        """
        testing creation of properties
        """
        self.property = {
            "name": "property 1",
            "description": "test description 1",
            "point": '11.0041125, -74.80917',
            "address": "buenavista, barranquilla"
        }
        response = self.client.post('/api/v1/houm/properties/', data=self.property, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_properties(self):
        """
        Implementation of factories with faker
        """
        new_property = PropertyFactory()
        response = self.client.get('/api/v1/houm/properties/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_send_coordinates_houmer(self):
        """
        testing the coordinates sending for the houmers (most of the logic happens here in the model)
        """
        self.coordinates_houmer = {
            "point": '11.0041125, -74.80917',
        }
        response = self.client.post('/api/v1/houm/historical_locations/', data=self.coordinates_houmer, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
