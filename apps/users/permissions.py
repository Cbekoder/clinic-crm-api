from rest_framework.permissions import BasePermission


class IsCEO(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "SuperStatus" or request.user.is_superuser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role == "Staff" and request.user.is_staff) or request.user.is_superuser

class IsRegistrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role == "Staff" and request.user.is_staff) or request.user.is_superuser

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role == "Staff" and request.user.is_staff) or request.user.is_superuser
