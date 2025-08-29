from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "photo", "real_name"]
        read_only_fields = ["id", "role"]  #Prevent students editing role
