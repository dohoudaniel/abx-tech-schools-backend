# Courses App

This app manages the academic courses offered by the school.

## Features
- **Course Details**: Title and optional description.
- **Teacher Assignment**: Each course is linked to exactly one teacher (One-to-Many).
- **Nested Data**: API responses include serialized teacher details for better frontend integration.
- **API Endpoints**: CRUD support via `/api/courses/`.

## Components
- `models.py`: `Course` model with foreign key to `Teacher`.
- `serializers.py`: `CourseSerializer` (includes nested `TeacherSerializer`).
- `views.py`: `CourseViewSet`.
