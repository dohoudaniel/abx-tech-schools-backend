from rest_framework import viewsets
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing enrollment instances.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
