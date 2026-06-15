import os
import random

from django.test import TestCase
from pyexpat import features
from rest_framework import status
from social_core.pipeline import user

from authentication.models import User

from ..api.views import ReservationApiView
from ..models import Reservation
from table.models import Table, Feature
from django.urls import reverse


class BookTableTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.COUNT_FEATURES = 5
        cls.COUNT_TABLES = 10
        cls.COUNT_RESERVATIONS = 3
        cls.user1 = User.objects.create_user(username='test1', password='test1')
        cls.user2 = User.objects.create_user(username='test2', password='test2')
        available_photos = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
        features = [Feature.objects.create(name=f"Тег {i}") for i in range(1, cls.COUNT_FEATURES + 1)]
        for i in range(1, cls.COUNT_TABLES + 1):
            random_photo = random.choice(available_photos)
            photo_path = os.path.join('table_image', random_photo)
            table = Table.objects.create(
                number=i,
                image=photo_path,
                seats=random.randint(1, 10),
                description=f"Описание {i}",
            )
            table.feature.add(random.choice(features))
        cls.reservation_data = {
            "date": "2029-11-03",
            "hour_start": 10,
            "hour_end": 16,
            "table": random.randint(1, 10)
        }
        cls.reservation_creat_and_list_url = reverse("reservation-list")

    def test_create_reservation_anon(self):
        resp = self.client.post(self.reservation_creat_and_list_url, data=self.reservation_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation(self):
        self.client.force_login(self.user1)
        resp = self.client.post(self.reservation_creat_and_list_url, data=self.reservation_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), self.COUNT_TABLES)
        self.assertEqual(Feature.objects.count(), self.COUNT_FEATURES)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_delete_not_own_reservation(self):
        self.client.force_login(self.user2)
        resp = self.client.post(self.reservation_creat_and_list_url, data=self.reservation_data)
        reservation_id = resp.data.get("id")
        print("reservation id: ", reservation_id)
        self.client.force_login(self.user1)
        url = reverse("reservation-detail", kwargs={"id": reservation_id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_reservation(self):
        self.client.force_login(self.user2)
        resp = self.client.post(self.reservation_creat_and_list_url, data=self.reservation_data)
        reservation_id = resp.data.get("id")
        url = reverse("reservation-detail", kwargs={"id": reservation_id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_reservations(self):
        self._create_N_reservation(self.COUNT_RESERVATIONS)
        resp = self.client.get(self.reservation_creat_and_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.count(), self.COUNT_RESERVATIONS)
        self.assertIn("results", resp.data)
        self.assertIn("next", resp.data)
        self.assertEqual(len(resp.data.get("results")), self.COUNT_RESERVATIONS)

    def _create_reservation(self):
        resp = self.client.post(self.reservation_creat_and_list_url, data=self.reservation_data)

    def _create_N_reservation(self, n: int):
        self.client.force_login(self.user1)
        for i in range(n):
            self._create_reservation()
