from django.db import models
from django.contrib.auth.models import AbstractUser

#User class with role category to designate between student and teacher
class User(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True) #Photo file is uploaded and stored 
    real_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications") #The recipient of notification
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) #To mark notifications as seen and reduce the visual space they take up in UI
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True) #Course from which notification originated (ie. Student enrolled in course or new material for course from teacher)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"