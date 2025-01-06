from rest_framework.permissions import BasePermission

class IsCEOOrAdminOrDoctorOrRegistrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role in ['ceo', 'admin', 'doctor', 'registrator'] or request.user.is_superuse

class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "ceo"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "admin"

class IsRegistrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "registrator"

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "doctor"
