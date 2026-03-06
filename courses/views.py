from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from core.permissions import IsTeacher, IsCourseTeacherOrReadOnly
from teachers.models import Teacher
from enrollments.models import Enrollment
from students.serializers import StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacher, IsCourseTeacherOrReadOnly]
        elif self.action == 'students':
            permission_classes = [IsTeacher, IsCourseTeacherOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Assign the currently authenticated teacher to the new course.
        """
        teacher = Teacher.objects.get(email=self.request.user.email)
        serializer.save(teacher=teacher)
        
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Gets a list of students enrolled in this specific course. (Teacher only)
        """
        course = self.get_object()
        
        # Verify the requesting teacher is the owner of the course
        if course.teacher.email != request.user.email:
            return Response(
                {"detail": "You do not have permission to view students of a course you don't teach."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        enrollments = Enrollment.objects.filter(course=course).select_related('student')
        students = [enrollment.student for enrollment in enrollments]
        
        # Serialize the students manually or use the existing StudentSerializer
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
