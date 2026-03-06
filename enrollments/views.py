from rest_framework import viewsets, permissions, exceptions
from .models import Enrollment
from .serializers import EnrollmentSerializer
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing enrollment instances.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Enrollment.objects.none()
            
        if user.is_superuser:
            return Enrollment.objects.all()

        # If user is a student, they see their own enrollments
        if Student.objects.filter(email=user.email).exists():
            return Enrollment.objects.filter(student__email=user.email)
            
        # If user is a teacher, they see enrollments for their courses
        elif Teacher.objects.filter(email=user.email).exists():
            return Enrollment.objects.filter(course__teacher__email=user.email)
            
        # If user is a parent, they see enrollments for their linked students
        elif Parent.objects.filter(email=user.email).exists():
            parent = Parent.objects.get(email=user.email)
            return Enrollment.objects.filter(student__parents=parent)
            
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        """
        Assign the currently authenticated student to the new enrollment.
        Teachers are not allowed to enroll in courses.
        """
        try:
            student = Student.objects.get(email=self.request.user.email)
        except Student.DoesNotExist:
            raise exceptions.PermissionDenied("Only students can enroll in courses.")
            
        course = serializer.validated_data['course']
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise exceptions.ValidationError({"detail": "You are already enrolled in this course."})
            
        serializer.save(student=student)
