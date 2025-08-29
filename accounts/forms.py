from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .validators import validate_username_unique, validate_email_unique

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'real_name', 'photo']
        
    #Clean username and check that it is unique
    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username_unique(username)
        return username

    #Clean email and check that it is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email_unique(email)
        return email

    #Store user information
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

#Same as above 
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'real_name', 'photo']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username_unique(username)
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email_unique(email)
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
        return user