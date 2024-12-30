from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User, NoteGroup

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name', read_only=True)
    notes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='note'
    )
    note_group = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=NoteGroup.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'first_name', 'last_name', 
            'email', 'role', 'is_active', 'last_active_at', 
            'date_joined', 'notes', 'note_group'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_active_at': {'read_only': True},
            'date_joined': {'read_only': True}
        }

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 