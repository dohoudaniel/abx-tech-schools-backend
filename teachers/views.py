from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing teacher instances.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
