from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from authentication.models import User


class AuthTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "testuser1",
            "password": "test1123456789876543",
        }
        cls.admin = User.objects.create_user(username="admin", password="admin", is_staff=True, is_superuser=False)
        cls.user = User.objects.create_user(username="user", password="user1234")
        cls.user_list_create_url = reverse('api_users:user-list')

    def test_registration_default_user(self):
        resp = self.client.post(self.user_list_create_url, data=self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_list_default_user(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.user_list_create_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_admin(self):
        self.client.force_login(self.admin)
        resp = self.client.get(self.user_list_create_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
