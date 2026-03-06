from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Teacher
from .serializers import TeacherSerializer
from students.models import Student
from students.serializers import StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing teacher instances.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=False, methods=['get'], url_path='my-students')
    def my_students(self, request):
        # Find the teacher profile associated with the current user's email
        try:
            teacher = Teacher.objects.get(email=request.user.email)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher profile not found."}, status=404)

        # Get all students enrolled in any course taught by this teacher
        # Course -> ForeignKey(Teacher, related_name='courses')
        # Enrollment -> ForeignKey(Course, related_name='enrollments')
        # Enrollment -> ForeignKey(Student, related_name='enrollments')
        
        students = Student.objects.filter(
            enrollments__course__teacher=teacher
        ).distinct()

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
