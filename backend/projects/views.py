from rest_framework import viewsets, permissions

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsProjectOwner


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        # Users only ever see their own projects — this is the core
        # authorization boundary, enforced at the queryset level, not
        # just via has_object_permission (belt and suspenders).
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)