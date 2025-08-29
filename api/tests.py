from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserApiTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teach1", password="pass", role="teacher")
        self.stud = User.objects.create_user(username="stud1", password="pass", role="student")

    def test_me_get(self): #Can users access their own data?
        self.client.login(username="stud1", password="pass")
        resp = self.client.get("/api/users/me/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "stud1")

    def test_list_requires_teacher(self): #Can students access data they are not supposed to?
        self.client.login(username="stud1", password="pass")
        resp = self.client.get("/api/users/")
        self.assertEqual(resp.status_code, 403)

        self.client.logout()
        self.client.login(username="teach1", password="pass") #Can teachers access all the data they are supposed to?
        resp = self.client.get("/api/users/")
        self.assertEqual(resp.status_code, 200)

    def test_retrieve_permissions(self): #Can students access other student's data?
        other = User.objects.create_user(username="stud2", password="pass", role="student")
        self.client.login(username="stud1", password="pass")
        resp = self.client.get(f"/api/users/{other.id}/")
        self.assertEqual(resp.status_code, 403)

        self.client.logout() #Can teachers access student data?
        self.client.login(username="teach1", password="pass")
        resp = self.client.get(f"/api/users/{other.id}/")
        self.assertEqual(resp.status_code, 200)