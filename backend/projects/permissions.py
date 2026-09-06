from rest_framework import permissions


class IsProjectOwner(permissions.BasePermission):
    """Only the project's owner can view or modify it."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user