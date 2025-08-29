from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(TestCase):
    def test_create_account_both_roles(self): #SETUP
        s = User.objects.create_user(username="stud", password="x", role="student")
        t = User.objects.create_user(username="teach", password="x", role="teacher")
        self.assertEqual(s.role, "student")
        self.assertEqual(t.role, "teacher")

    def test_username_unique(self): #Make sure that non-unique usernames cannot be created
        User.objects.create_user(username="dup", password="x", role="student")
        with self.assertRaises(Exception):
            User.objects.create_user(username="dup", password="x", role="teacher")

    def test_login_logout(self): #Test login and logout functionality
        u = User.objects.create_user(username="u1", password="p", role="student")
        ok = self.client.login(username="u1", password="p")
        self.assertTrue(ok)
        self.client.logout()
