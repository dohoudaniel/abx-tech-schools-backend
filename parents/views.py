from rest_framework import viewsets, permissions, exceptions
from .models import Parent, ParentStudent
from .serializers import ParentSerializer, ParentStudentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing parent instances.
    """
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Parent.objects.all()
        
        # If the user is a parent, they only see their own profile
        if user.role == 'parent':
            return Parent.objects.filter(email=user.email)
            
        # Admins, students (maybe?), teachers see based on their specific needs.
        # For phase 1, we let it be filtered for visibility.
        return Parent.objects.all()

class ParentStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing parent-student link instances (junction).
    """
    serializer_class = ParentStudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ParentStudent.objects.all()
            
        if user.role == 'parent':
            return ParentStudent.objects.filter(parent__email=user.email)
            
        if user.role == 'student':
            return ParentStudent.objects.filter(student__email=user.email)
            
        return ParentStudent.objects.all()
