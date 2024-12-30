from rest_framework import serializers
from .models import Note, NoteGroup

class NoteGroupSerializer(serializers.ModelSerializer):
    note_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = NoteGroup
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 
                 'note_count', 'member_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_note_count(self, obj):
        return obj.notes.count()

    def get_member_count(self, obj):
        # 暂时返回固定值，后续可以根据实际需求实现
        return 1

class NoteSerializer(serializers.ModelSerializer):
    group_detail = NoteGroupSerializer(source='group', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'group', 'group_detail', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 