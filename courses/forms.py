from django import forms
from .models import Course, Feedback, CourseMaterial

#Teacher does not have to be included because it is automatically set as the teacher creating the course in views
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave your feedback...'}),
        }
        
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['file', 'description']
        
class CourseNotificationForm(forms.Form):
    course = forms.ModelChoiceField(queryset=None, label="Select Course")
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Notification Message")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'teacher':
            self.fields['course'].queryset = user.teacher_courses.all()
        else:
            self.fields['course'].queryset = Course.objects.none()