from rest_framework import permissions


class IsAdminOrCreateReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "PUT":
            return request.user.is_superuser
        return request.user
