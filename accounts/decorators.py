from django.core.exceptions import PermissionDenied

#Decorator for function to require student role
def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

#Decorator for function to require teacher role
def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper