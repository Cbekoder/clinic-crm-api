from rest_framework.permissions import BasePermission


class IsCEOOrAdminOrDoctorOrRegistrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role in ['ceo', 'admin', 'doctor',
                                      'registrator'] or request.user.is_superuser) and request.user.status == "active"


class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "ceo" and request.user.status == "active"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "admin" and request.user.status == "active"


class IsRegistrator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "registrator" and request.user.status == "active"


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "doctor" and request.user.status == "active"
