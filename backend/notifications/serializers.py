from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    task_title = serializers.ReadOnlyField(source='task.title')

    class Meta:
        model = Notification
        fields = ['id', 'task', 'task_title', 'notification_type', 'message', 'created_at', 'read']
        read_only_fields = ['id', 'task', 'task_title', 'notification_type', 'message', 'created_at']