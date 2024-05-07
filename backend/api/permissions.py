from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsTeacherUser(permissions.BasePermission):
    """
    Allows access only to teachers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


class IsStudentUser(permissions.BasePermission):
    """
    Allows access only to students.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsParentUser(permissions.BasePermission):
    """
    Allows access only to parents.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "parent"
