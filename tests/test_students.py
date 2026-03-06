from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import User
from students.models import Student

class StudentTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@test.com', password='password123')
        self.student_user = User.objects.create_user(email='student@test.com', password='password123')
        self.student = Student.objects.create(email='student@test.com', first_name='John', last_name='Doe', gender='M')
        self.student_list_url = '/api/students/'

    def test_list_students_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.student_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_students_unauthenticated(self):
        response = self.client.get(self.student_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_student(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@test.com',
            'gender': 'F'
        }
        response = self.client.post(self.student_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_student_gender_choices(self):
        self.client.force_authenticate(user=self.admin_user)
        # Invalid gender choice 'X'
        data = {
            'first_name': 'Bob',
            'last_name': 'Brown',
            'email': 'bob@test.com',
            'gender': 'X'
        }
        response = self.client.post(self.student_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gender', response.data)
