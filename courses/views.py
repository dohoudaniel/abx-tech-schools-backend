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
        
    @action(detail=False, methods=['get'], url_path='my-courses')
    def my_courses(self, request):
        """
        Gets a list of courses taught by the currently authenticated teacher.
        """
        try:
            teacher = Teacher.objects.get(email=request.user.email)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher profile not found."}, status=404)
            
        courses = Course.objects.filter(teacher=teacher)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

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
