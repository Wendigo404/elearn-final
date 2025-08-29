
from django.db import models
from django.conf import settings
from accounts.models import User
from courses.models import Course

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}"
