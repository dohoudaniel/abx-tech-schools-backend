# ABX Tech Schools - API Documentation

This document outlines the API endpoints available in the LMS backend. Base URL assumes local development: `http://localhost:8000`.

## 🔒 Authentication

This API uses **JSON Web Tokens (JWT)** for authentication. Protected endpoints require the `Authorization` header with a Bearer token:
`Authorization: Bearer <your_access_token>`

### 1. Login (Get Token)
- **Endpoint:** `POST /api/auth/login/`
- **Description:** Authenticate a user and receive an access/refresh token pair.
- **Request Body:**
  ```json
  {
    "email": "student@student.edu",
    "password": "password123"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "access": "eyJhbGci...<access token>...",
    "refresh": "eyJhbGci...<refresh token>..."
  }
  ```

### 2. Refresh Token
- **Endpoint:** `POST /api/auth/token/refresh/`
- **Description:** Obtain a new access token using a valid refresh token.
- **Request Body:**
  ```json
  {
    "refresh": "eyJhbGci...<refresh token>..."
  }
  ```

---

## 👨‍🏫 Teachers

### 1. List Teachers
- **Endpoint:** `GET /api/teachers/`
- **Access:** Authenticated Users
- **Description:** Retrieves a list of all teachers in the system.

### 2. Retrieve a Specific Teacher
- **Endpoint:** `GET /api/teachers/{id}/`
- **Access:** Authenticated Users

---

## 🎓 Students

### 1. List Students
- **Endpoint:** `GET /api/students/`
- **Access:** Authenticated Users
- **Description:** Retrieves a list of all students.

### 2. Retrieve a Specific Student
- **Endpoint:** `GET /api/students/{id}/`
- **Access:** Authenticated Users

---

## 📚 Courses

### 1. List All Courses
- **Endpoint:** `GET /api/courses/`
- **Access:** Authenticated Users
- **Description:** Returns all courses. The JSON response embeds full teacher details automatically.
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "title": "Mathematics",
      "description": "Math course...",
      "teacher": 1,
      "teacher_details": {
        "id": 1,
        "first_name": "Ade",
        "last_name": "Olawale",
        "email": "ade.olawale@school.edu",
        "gender": "M"
      },
      "created_at": "2024-03-06T10:00:00Z"
    }
  ]
  ```

### 2. Create a Course
- **Endpoint:** `POST /api/courses/`
- **Access:** **Teachers Only**
- **Description:** Creates a new course. The teacher is automatically inferred from the authenticated user token.
- **Request Body:**
  ```json
  {
    "title": "Introduction to Physics",
    "description": "Basic concepts of mechanics."
  }
  ```

### 3. Update a Course
- **Endpoint:** `PATCH /api/courses/{id}/`
- **Access:** **Teachers Only (Specifically the teacher who owns the course)**
- **Description:** Edits course details.

### 4. Get Enrolled Students for a Course
- **Endpoint:** `GET /api/courses/{id}/students/`
- **Access:** **Teachers Only (Specifically the teacher who owns the course)**
- **Description:** Retrieves a list of all students currently enrolled in this particular course.
- **Response Example:**
  ```json
  [
    {
      "id": 10,
      "first_name": "Victor",
      "last_name": "Okafor",
      "email": "victor.okafor@student.edu",
      "gender": "M",
      "date_of_birth": "2009-05-14"
    }
  ]
  ```

---

## 🎒 Enrollments

### 1. List Enrollments
- **Endpoint:** `GET /api/enrollments/`
- **Access:** Authenticated Users
- **Description:** 
  - **Students:** See only their own enrollments.
  - **Teachers:** See only enrollments for courses they teach.
  - Returns nested student and course details.

### 2. Enroll in a Course
- **Endpoint:** `POST /api/enrollments/`
- **Access:** **Students Only**
- **Description:** Enroll the authenticated student in a course. The system will prevent duplicate enrollments (Status `400 Bad Request` if already enrolled).
- **Request Body:**
  ```json
  {
    "course": 2
  }
  ```

### 3. Drop a Course (Unenroll)
- **Endpoint:** `DELETE /api/enrollments/{enrollment_id}/`
- **Access:** **Students Only (for their own enrollments)**
- **Description:** Deletes the specific enrollment record.

---

## 👨‍👩‍👦 Parents

### 1. List Parents
- **Endpoint:** `GET /api/parents/`
- **Access:** Authenticated Users
- **Description:** Retrieves a list of all parents. Parents see only their own profile.

### 2. Retrieve a Specific Parent
- **Endpoint:** `GET /api/parents/{id}/`
- **Access:** Authenticated Users
- **Description:** Returns parent details, including their linked students and specific relationship types.

### 3. List Parent-Student Links
- **Endpoint:** `GET /api/parents/links/`
- **Access:** Authenticated Users
- **Description:** 
  - **Parents:** See links to their children.
  - **Students:** See links to their parents.
  - Describes the `relationship` (e.g., Mother, Father, Guardian).

---

## 🛠️ Errors and Status Codes Reference
- **200 OK**: Request successful.
- **201 Created**: Resource successfully created.
- **400 Bad Request**: Validation error (e.g., enrolling in a course twice).
- **401 Unauthorized**: Missing, expired, or invalid JWT token.
- **403 Forbidden**: User does not have permission (e.g., student trying to create a course, or teacher trying to view students for a course they don't teach).
- **404 Not Found**: Resource doesn't exist.
