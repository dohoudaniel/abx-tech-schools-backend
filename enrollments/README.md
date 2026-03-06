# Enrollments App

This app manages the registration of students into courses.

## Features
- **Many-to-Many Bridge**: Implements the relationship between students and courses.
- **Uniqueness**: Prevents duplicate enrollments for the same student in the same course.
- **Detailed Responses**: API responses provide details for both the student and the course.
- **API Endpoints**: CRUD support via `/api/enrollments/`.

## Components
- `models.py`: `Enrollment` model linking `Student` and `Course`.
- `serializers.py`: `EnrollmentSerializer`.
- `views.py`: `EnrollmentViewSet`.
