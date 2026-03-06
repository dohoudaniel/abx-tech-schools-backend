from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import User
from teachers.models import Teacher

class TeacherTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@test.com', password='password123')
        self.teacher_user = User.objects.create_user(email='teacher@test.com', password='password123')
        self.teacher = Teacher.objects.create(email='teacher@test.com', first_name='Tom', last_name='Jones', gender='M')
        self.teacher_list_url = '/api/teachers/'

    def test_list_teachers_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.teacher_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_teacher(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'email': 'sarah@test.com',
            'gender': 'F'
        }
        response = self.client.post(self.teacher_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)

    def test_teacher_gender_choices(self):
        self.client.force_authenticate(user=self.admin_user)
        # Invalid gender choice 'Y'
        data = {
            'first_name': 'Kyle',
            'last_name': 'Reese',
            'email': 'kyle@test.com',
            'gender': 'Y'
        }
        response = self.client.post(self.teacher_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gender', response.data)
