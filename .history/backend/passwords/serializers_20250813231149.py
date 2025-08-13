from rest_framework import serializers
from .models import PasswordEntry

class PasswordEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordEntry
        fields = ['id', 'site_name', 'site_url', 'username', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']