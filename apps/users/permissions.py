from rest_framework.permissions import BasePermission


class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == "ceo" or request.user.is_superuser
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == "admin"
        return False

class IsRegistrator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == "registrator"
        return False

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == "doctor"
        return False