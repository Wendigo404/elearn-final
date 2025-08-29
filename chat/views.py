from django.shortcuts import render, get_object_or_404
from .models import ChatMessage
from courses.models import Course

def course_chat(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    messages = ChatMessage.objects.filter(course=course).select_related("sender")
    return render(request, "chat/course_chat.html", {
        "course": course,
        "messages": messages,
    })