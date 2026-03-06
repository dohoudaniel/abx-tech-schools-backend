from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
