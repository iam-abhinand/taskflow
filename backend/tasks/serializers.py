from rest_framework import serializers
from .models import Task
from projects.models import Project


class TaskSerializer(serializers.ModelSerializer):
    assignee_username = serializers.ReadOnlyField(source='assignee.username')

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 'status',
            'assignee', 'assignee_username', 'due_date',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_project(self, project):
        # Prevent creating a task under a project you don't own.
        request = self.context['request']
        if project.owner != request.user:
            raise serializers.ValidationError("You do not have access to this project.")
        return project