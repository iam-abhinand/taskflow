from rest_framework import viewsets, permissions

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskProjectOwner


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskProjectOwner]

    def get_queryset(self):
        # Same pattern as projects: scope at the queryset level so a user
        # never even sees tasks belonging to someone else's project.
        return Task.objects.filter(project__owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context