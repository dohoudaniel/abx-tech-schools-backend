# ABX Tech Schools LMS Backend

This is the backend for the ABX Tech Schools Learning Management System (LMS), built with Django and Django REST Framework.

## Features (Phase 1)

- **Student Management**: CRUD operations for students.
- **Teacher Management**: CRUD operations for teachers.
- **Course Management**: Links courses to teachers (One-to-Many).
- **Enrollment System**: Junction system for many-to-many relationships between students and courses.
- **Modern Authentication**: Email-based login using JWT (SimpleJWT).
- **Interactive API Documentation**: Full Swagger UI and ReDoc integration.
- **Production-Ready Database**: Configured for Supabase (PostgreSQL) with `dj-database-url`.

> [!TIP]
> **Parents Feature**: A dedicated feature for parents is currently under development and can be found in the [`feature/parents`](../../tree/feature/parents) branch. It includes parent profiles and student-parent linking.

---

## 🛠️ Technology Stack

- **Framework**: [Django](https://www.djangoproject.com/) 5.0
- **API Engine**: [Django REST Framework](https://www.django-rest-framework.org/)
- **Auth**: [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- **Documentation**: [drf-spectacular](https://drf-spectacular.readthedocs.io/) (Swagger & ReDoc)
- **Database Support**: PostgreSQL (via Supabase) & SQLite
- **Environment**: Python Decouple / python-dotenv

---

## 📊 Database Schema (ERD)

The database follows a relational structure optimized for an LMS:

![ERD Diagram](./ERD.png)

### Relationship Logic
- **Teacher → Course**: One-to-Many (One teacher per course).
- **Student ↔ Course**: Many-to-Many (Implemented via the `enrollments` table).

---

## ⚙️ Setup and Installation

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (or Supabase)
- Virtual Environment (pipenv/venv)

### 2. Environment Variables
Create a `.env` file in the root directory and copy from `.env.example`:

```bash
cp .env.example .env
```

Define your credentials:
```env
SECRET_KEY=your_secret_key
DEBUG=True # Set to False in production
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 3. Installation
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the API
```bash
python manage.py runserver
```

---

## 📖 API Documentation

Once the server is running, you can access the documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

---

## 🔑 Test Credentials

To test the API with pre-seeded data, you can find a list of all teacher and student accounts here:
👉 **[View Test Credentials](./docs/CREDENTIALS.md)**

### Main Endpoints
| Feature | Endpoint | Method | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `/api/auth/login/` | POST | Login with email/password to get JWT |
| **Students** | `/api/students/` | GET/POST | List and create students |
| **Teachers** | `/api/teachers/` | GET/POST | List and create teachers |
| **Courses** | `/api/courses/` | GET/POST | Courses and their teachers |
| **Enrollments** | `/api/enrollments/` | GET/POST | Student course registrations |

---

## 🛡️ Security Note
- The Django Admin panel (`/admin/`) is **disabled** when `DEBUG=False` for enhanced production security.
- Token-based authentication (JWT) is required for all state-changing operations.
