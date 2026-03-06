from rest_framework import serializers
from .models import Course
from teachers.serializers import TeacherSerializer

class CourseSerializer(serializers.ModelSerializer):
    teacher_details = TeacherSerializer(source='teacher', read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'teacher', 'teacher_details', 'created_at')
        read_only_fields = ('teacher',)
