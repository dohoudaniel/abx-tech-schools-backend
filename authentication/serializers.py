from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent

class UserSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'profile_data')

    def get_profile_data(self, obj):
        if obj.role == 'student':
            student = Student.objects.filter(email=obj.email).first()
            if student:
                return {
                    'gender': student.get_gender_display() if student.gender else None,
                    'date_of_birth': student.date_of_birth,
                }
        elif obj.role == 'teacher':
            teacher = Teacher.objects.filter(email=obj.email).first()
            if teacher:
                return {
                    'gender': teacher.get_gender_display() if teacher.gender else None,
                }
        elif obj.role == 'parent':
            parent = Parent.objects.filter(email=obj.email).first()
            if parent:
                return {
                    'gender': parent.get_gender_display() if parent.gender else None,
                    'family_last_name': parent.family_last_name,
                }
        return {}

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
