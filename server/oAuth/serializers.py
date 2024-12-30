from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'name')

    def get_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 