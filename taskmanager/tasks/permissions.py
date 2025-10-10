from rest_framework import permissions

# allow only object owners to access or modify their data
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    