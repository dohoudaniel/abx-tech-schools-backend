from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import User
from teachers.models import Teacher
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

class EnrollmentTestCase(APITestCase):
    def setUp(self):
        # Create users
        self.teacher_user = User.objects.create_user(email='teacher@test.com', password='password123')
        self.student_user = User.objects.create_user(email='student@test.com', password='password123')
        self.student2_user = User.objects.create_user(email='student2@test.com', password='password123')

        # Create profiles
        self.teacher = Teacher.objects.create(email='teacher@test.com', first_name='T1', last_name='L1')
        self.student = Student.objects.create(email='student@test.com', first_name='S1', last_name='L1')
        self.student2 = Student.objects.create(email='student2@test.com', first_name='S2', last_name='L2')

        # Create course
        self.course = Course.objects.create(title='Course 1', teacher=self.teacher)

        self.enrollment_list_url = '/api/enrollments/'

    def test_student_can_enroll_in_course(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'course': self.course.id}
        response = self.client.post(self.enrollment_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(Enrollment.objects.first().student, self.student)

    def test_teacher_cannot_enroll_in_course(self):
        self.client.force_authenticate(user=self.teacher_user)
        data = {'course': self.course.id}
        response = self.client.post(self.enrollment_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_student_cannot_enroll_twice(self):
        self.client.force_authenticate(user=self.student_user)
        Enrollment.objects.create(course=self.course, student=self.student)
        
        data = {'course': self.course.id}
        response = self.client.post(self.enrollment_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_teacher_can_view_enrolled_students(self):
        # Create an enrollment
        Enrollment.objects.create(course=self.course, student=self.student)
        Enrollment.objects.create(course=self.course, student=self.student2)
        
        self.client.force_authenticate(user=self.teacher_user)
        students_url = f'/api/courses/{self.course.id}/students/'
        response = self.client.get(students_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        emails = [s['email'] for s in response.data]
        self.assertIn(self.student.email, emails)
        self.assertIn(self.student2.email, emails)

    def test_teacher_cannot_view_students_of_other_course(self):
        # Create another teacher and try to view the first teacher's course students
        teacher2_user = User.objects.create_user(email='teacher2@test.com', password='password123')
        Teacher.objects.create(email='teacher2@test.com', first_name='T2', last_name='L2')
        
        Enrollment.objects.create(course=self.course, student=self.student)
        
        self.client.force_authenticate(user=teacher2_user)
        students_url = f'/api/courses/{self.course.id}/students/'
        response = self.client.get(students_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
