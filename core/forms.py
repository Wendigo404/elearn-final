from django import forms
from .models import StatusUpdate

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind"}),
        }
        labels = {
            'content': '',
        }