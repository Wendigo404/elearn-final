from rest_framework import viewsets, permissions, response, decorators
from accounts.models import User
from .serializers import UserSerializer
from .permissions import teacherPrivilege

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [teacherPrivilege]

    #List should only be available to teachers
    def list(self, request, *args, **kwargs):
        if request.user.role != "teacher":
            return response.Response(
                {"detail": "Only teachers can view all users."},
                status=403
            )
        return super().list(request, *args, **kwargs)


    #/api/users/me/
    @decorators.action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return response.Response(serializer.data)