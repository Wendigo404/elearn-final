from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignUpForm, TeacherSignUpForm

def student_signup(request): #Signup form for students
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, './signup.html', {'form': form, 'user_type': 'Student'})

def teacher_signup(request): #Signup form for teachers
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_home')
    else:
        form = TeacherSignUpForm()
    return render(request, './signup.html', {'form': form, 'user_type': 'Teacher'})
