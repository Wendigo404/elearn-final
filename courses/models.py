from django.db import models
from accounts.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='teacher_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', limit_choices_to={'role': 'student'}, blank=True)
    blocked_students = models.ManyToManyField(User, related_name='blocked_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Feedback(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="feedbacks")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback by {self.student.username} on {self.course.title}"
    

class CourseMaterial(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_materials/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.file.name}"