from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import StatusUpdate  # adjust path if different

User = get_user_model()

class StatusUpdateTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="s1", password="p", role="student")

    def test_post_status(self):
        self.client.login(username="s1", password="p")
        resp = self.client.post(reverse("home"), {"content": "Hello world", "status_submit": "1"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(StatusUpdate.objects.filter(user=self.student, content__icontains="Hello").exists())
