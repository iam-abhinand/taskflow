from rest_framework import permissions


class IsTaskProjectOwner(permissions.BasePermission):
    """Only the owner of the task's parent project can view or modify it."""

    def has_object_permission(self, request, view, obj):
        return obj.project.owner == request.user