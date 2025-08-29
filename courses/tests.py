from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class CourseBasicsTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="t1", password="p", role="teacher")
        self.student = User.objects.create_user(username="s1", password="p", role="student")
        self.course = Course.objects.create(title="Maths", description="Desc", teacher=self.teacher)

    def test_teacher_can_create_course(self): #Can teachers create a new course?
        self.client.login(username="t1", password="p")
        resp = self.client.post(reverse("create_course"), {"title": "Physics", "description": "D"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Course.objects.filter(title="Physics", teacher=self.teacher).exists())

    def test_student_cannot_create_course(self): #Can students create a course?
        self.client.login(username="s1", password="p")
        resp = self.client.get(reverse("create_course"))
        self.assertIn(resp.status_code, (302, 403))

    def test_student_enrolls(self): #Can students enroll in a course?
        self.client.login(username="s1", password="p")
        resp = self.client.post(reverse("enroll_course", args=[self.course.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(self.student, self.course.students.all())

    def test_teacher_can_block_student(self): #Can a teacher block a student?
        self.client.login(username="t1", password="p")
        resp = self.client.post(reverse("block_student", args=[self.student.id, self.course.id]))
        self.assertIn(resp.status_code, (302, 200))
        self.assertNotIn(self.student, self.course.students.all())
