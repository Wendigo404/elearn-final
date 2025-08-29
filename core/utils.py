from accounts.models import Notification

#Alert all students in a specific course
def send_course_notification(teacher, course, message):
    if course in teacher.teacher_courses.all():
        for student in course.students.all():
            Notification.objects.create(user=student, message=message, course=course)
        return True
    return False
