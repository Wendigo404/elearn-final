from rest_framework import permissions
#API permissions to allow users to only access own data unless teacher role
class teacherPrivilege(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                obj == request.user or
                getattr(request.user, "role", None) == "teacher" 
            )
        return obj == request.user
