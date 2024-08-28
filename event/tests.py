from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Event
from django.utils import timezone
from datetime import timedelta


class EventAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="admin")
        self.client.force_login(self.user)
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=2),
            created_by=self.user
        )

    def test_get_events(self):
        url = reverse("events-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Event")

    def test_update_event(self):
        url = reverse("events-detail", kwargs={"pk": self.event.pk})
        data = {
            "name": "Updated Event Name",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Updated Event Name")

    def test_register_to_event(self):
        url = reverse("events-register", kwargs={"pk": self.event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user in self.event.subscribers.all())

    def test_unregister_from_event(self):
        self.event.subscribers.add(self.user)
        url = reverse("events-unregister", kwargs={"pk": self.event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user in self.event.subscribers.all())

    def test_register_to_past_event(self):
        past_event = Event.objects.create(
            name="Past Event",
            description="This is a past event",
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=1),
            created_by=self.user
        )
        url = reverse("events-register", kwargs={"pk": past_event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unregister_from_past_event(self):
        past_event = Event.objects.create(
            name="Past Event",
            description="This is a past event",
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=1),
            created_by=self.user
        )
        past_event.subscribers.add(self.user)
        url = reverse("events-unregister", kwargs={"pk": past_event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
