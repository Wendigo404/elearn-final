from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

#Both validators check that entered field is unique
def validate_username_unique(username):
    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError("This username is already taken")

def validate_email_unique(email):
    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError('This email is already in use')