from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import teacher_required, student_required
from .models import Course, Feedback, CourseMaterial
from .forms import *
from accounts.models import Notification, User
from django.http import HttpResponseForbidden, FileResponse
from chat.models import ChatMessage
import os


@login_required
@teacher_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user #teacher who created course is automatically set as courses teacher
            course.save()
            return redirect('browse_courses')
    else:
        form = CourseForm()
    return render(request, 'courses/create.html', {'form': form})

@login_required
def browse_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/browse.html', {'courses': courses, 'user': request.user})

@login_required
@student_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user in course.blocked_students.all():
        return redirect('home')
    
    if request.user not in course.students.all():
        course.students.add(request.user)

        Notification.objects.create(
            user=course.teacher,
            message=f"{request.user.username} has enrolled in {course.title}",
            course=course
        )
    
    return redirect('home')

@login_required
@teacher_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return redirect('browse_courses')
    if request.method == 'POST':
        course.delete()
        return redirect('browse_courses')
    return redirect('browse_courses')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST' and request.user.role == 'student':
        if request.user in course.students.all():
            messages.warning(request, "You are already enrolled in this course.")
        else:
            course.students.add(request.user)
            messages.success(request, f"You have been enrolled in {course.title}.")
        return redirect('course_detail', course_id=course.id)

    students = course.students.all()
    teacher = course.teacher

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'students': students,
        'teacher': teacher
    })

@login_required  
def course_detail_feedback(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    feedbacks = course.feedbacks.all()

    if request.method == "POST" and request.user.role == "student":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            return redirect("course_detail", course_id=course.id)
    else:
        form = FeedbackForm()

    return render(request, "courses/course_detail.html", {
        "course": course,
        "feedbacks": feedbacks,
        "form": form,
    })
    
@login_required
@teacher_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.teacher != request.user:
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.uploaded_by = request.user
            material.save()
            
            for student in course.students.all():
                Notification.objects.create(
                    user=student,
                    message=f"New material uploaded in {course.title}: {material.description or material.file.name}"
                )
            
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseMaterialForm()

    return render(request, 'courses/upload_material.html', {'form': form, 'course': course})



@login_required
def download_material(request, course_id):
    material = get_object_or_404(CourseMaterial, id=course_id)
    course = material.course

    #Only teacher or enrolled students can download
    if request.user != course.teacher and request.user not in course.students.all():
        return HttpResponseForbidden("You are not enrolled in this course.")

    file_handle = material.file.open("rb")
    response = FileResponse(file_handle, as_attachment=True, filename=os.path.basename(material.file.name))
    return response

@login_required
@teacher_required
def block_student(request, student_id, course_id):
    student = get_object_or_404(User, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    if request.user == course.teacher:
        course.students.remove(student)  #Blocked students are automatically unenrolled
        course.blocked_students.add(student)
        Notification.objects.create(
            user=student,
            course=course,
            message=f"You have been blocked from {course.title}."
        )
    return redirect('profile', username=student.username)

@login_required
@teacher_required
def unblock_student(request, student_id, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(User, id=student_id, role="student")

    #Only course teacher can restore blocked student access
    if request.user == course.teacher:
        if student in course.blocked_students.all():
            course.blocked_students.remove(student)

    return redirect("profile", username=student.username)


@login_required
def course_chat(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    messages = ChatMessage.objects.filter(course=course).select_related("sender")

    return render(request, 'courses/course_chat.html', {'course': course, "messages": messages})