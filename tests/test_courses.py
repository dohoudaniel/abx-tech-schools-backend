from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import User
from teachers.models import Teacher
from students.models import Student
from courses.models import Course

class CourseTestCase(APITestCase):
    def setUp(self):
        # Create users
        self.teacher_user = User.objects.create_user(email='teacher@test.com', password='password123')
        self.teacher2_user = User.objects.create_user(email='teacher2@test.com', password='password123')
        self.student_user = User.objects.create_user(email='student@test.com', password='password123')

        # Create profiles
        self.teacher = Teacher.objects.create(email='teacher@test.com', first_name='T1', last_name='L1')
        self.teacher2 = Teacher.objects.create(email='teacher2@test.com', first_name='T2', last_name='L2')
        self.student = Student.objects.create(email='student@test.com', first_name='S1', last_name='L1')

        # Create course
        self.course = Course.objects.create(title='Course 1', description='Desc 1', teacher=self.teacher)

        # URLs
        self.course_list_url = '/api/courses/'
        self.course_detail_url = f'/api/courses/{self.course.id}/'

    def test_teacher_can_create_course(self):
        self.client.force_authenticate(user=self.teacher_user)
        data = {'title': 'New Course', 'description': 'New Desc'}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(id=response.data['id']).teacher, self.teacher)

    def test_student_cannot_create_course(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'title': 'New Course by Student', 'description': 'student desc'}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)

    def test_teacher_can_edit_own_course(self):
        self.client.force_authenticate(user=self.teacher_user)
        data = {'title': 'Updated Course'}
        response = self.client.patch(self.course_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course')

    def test_teacher_cannot_edit_other_teachers_course(self):
        self.client.force_authenticate(user=self.teacher2_user)
        data = {'title': 'Hacked Course'}
        response = self.client.patch(self.course_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_edit_course(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'title': 'Hacked by Student'}
        response = self.client.patch(self.course_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_create_course(self):
        data = {'title': 'Hacked Course'}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
