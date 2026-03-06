from rest_framework import serializers
from .models import Parent, ParentStudent
from students.serializers import StudentSerializer

class ParentStudentSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    
    class Meta:
        model = ParentStudent
        fields = ('id', 'parent', 'student', 'student_details', 'relationship', 'linked_at')

class ParentSerializer(serializers.ModelSerializer):
    # This will allow us to see children when viewing a parent
    students_details = StudentSerializer(source='students', many=True, read_only=True)
    
    # We could also include the relationships via the through model records
    student_links = ParentStudentSerializer(source='parentstudent_set', many=True, read_only=True)
    
    class Meta:
        model = Parent
        fields = ('id', 'first_name', 'last_name', 'email', 'gender', 'family_last_name', 'created_at', 'students', 'students_details', 'student_links')
        read_only_fields = ('created_at',)
