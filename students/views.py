from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing student instances.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
