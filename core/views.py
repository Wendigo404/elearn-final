from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required
from .models import StatusUpdate
from accounts.models import User
from courses.models import Course
from django.db.models import Q
from .forms import StatusUpdateForm
from courses.forms import CourseNotificationForm
from accounts.models import Notification
from core.utils import send_course_notification

#login_required is used to obtain user value which is necessary for functiions

@login_required
def home(request):
    user = request.user

    #List all enrolled/taught courses
    if user.role == 'student':
        courses = user.enrolled_courses.all()
    elif user.role == 'teacher':
        courses = Course.objects.filter(teacher=user)
    else:
        courses = []

    status_form = StatusUpdateForm()
    notification_form = CourseNotificationForm(user=user) if user.role == 'teacher' else None

    if request.method == 'POST':
        #Status update form
        if 'status_submit' in request.POST:
            status_form = StatusUpdateForm(request.POST)
            if status_form.is_valid():
                status = status_form.save(commit=False)
                status.user = user
                status.save()
                return redirect('home')

        #Course notification form (teachers only)
        elif 'notification_submit' in request.POST and user.role == 'teacher':
            notification_form = CourseNotificationForm(request.POST, user=user)
            if notification_form.is_valid():
                course = notification_form.cleaned_data['course']
                message = notification_form.cleaned_data['message']
                send_course_notification(user, course, message)
                return redirect('home')

    #Load status updates and arrange by time of creation
    updates = StatusUpdate.objects.all().order_by('-created_at')

    return render(request, 'core/home.html', {
        'user': user,
        'courses': courses,
        'status_form': status_form,
        'notification_form': notification_form,
        'updates': updates
    })


def profile(request, username):
    user = get_object_or_404(User, username=username)

    if user.role == 'student':
        courses = user.enrolled_courses.all()
    elif user.role == 'teacher':
        courses = user.teacher_courses.all()
    else:
        courses = []
    
    
    updates = StatusUpdate.objects.filter(user=user).order_by('-created_at')

    return render(
        request,
        'core/profile.html',
        {
            'profile_user': user,
            'courses': courses,
            'status_updates': updates,
        }
    )

@login_required
@teacher_required #Only teachers are allowed to user search
def user_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(real_name__icontains=query)
        )
    
    return render(request, 'core/search.html', {'results': results, 'query': query})

@login_required
@teacher_required #Teachers can remove status updates
def delete_update(request, update_id):
    update = get_object_or_404(StatusUpdate, id=update_id)
    if request.method == 'POST':
        update.delete()
        return redirect('home')
    
@login_required
def mark_notification_read(request, notification_id):
    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    note.is_read = True
    note.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))