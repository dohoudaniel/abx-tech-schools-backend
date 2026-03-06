from rest_framework import permissions
from teachers.models import Teacher
from students.models import Student

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers to access the view.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Teacher.objects.filter(email=request.user.email).exists()

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Student.objects.filter(email=request.user.email).exists()

class IsCourseTeacherOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow the teacher of a course to edit it.
    Assumes the model instance has a `teacher` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `teacher`.
        # The teacher's email must match the request user's email.
        if hasattr(obj, 'teacher'):
            return obj.teacher.email == request.user.email
        return False
