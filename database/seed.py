import os
import django
import random
import sys
from datetime import date, timedelta
from pathlib import Path

# Add the project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from authentication.models import User
from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from enrollments.models import Enrollment

def run():
    print("🧹 Cleaning existing database records (excluding superusers)...")
    Enrollment.objects.all().delete()
    Course.objects.all().delete()
    Student.objects.all().delete()
    Teacher.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    print("👨‍🏫 Seeding Teachers and Courses...")
    # NOTE: Since DB rule states a course can only have ONE teacher, 
    # Ade and Bolu will each have their own variation of "Further Mathematics" classes.
    teacher_data = [
        ("Ade", "Olawale", "M", ["Mathematics", "Further Mathematics (Advanced)"]),
        ("Bolu", "Rios", "F", ["Biology", "Further Mathematics (Standard)"]),
        ("Cynthia", "Thawne", "F", ["English"]),
        ("Daniel", "Dohou", "M", ["Physics", "Chemistry"]),
    ]

    all_courses = []

    for first, last, gender, subjects in teacher_data:
        email = f"{first.lower()}.{last.lower()}@school.edu"
        # 1. Create User
        user = User.objects.create_user(
            email=email, 
            password="password123", 
            role='teacher',
            first_name=first,
            last_name=last
        )
        # 2. Create Teacher profile
        teacher = Teacher.objects.create(email=email, first_name=first, last_name=last, gender=gender)
        
        # 3. Create Courses for this teacher
        for sub in subjects:
            course = Course.objects.create(
                title=sub, 
                description=f"{sub} course, taught expertly by {first} {last}.", 
                teacher=teacher
            )
            all_courses.append(course)

    print("🎓 Seeding Students...")
    student_data = [
        ("Barry", "Allen", "M"),
        ("Iris", "Allen", "F"),
        ("Joe", "West", "M"),
        ("Wally", "West", "M"),
        ("Jane", "Lundberg", "F"),
        ("Elana", "Vance", "F"),
        ("Beatrix", "Wilde", "F"),
        ("Caleb", "Irons", "M"),
        ("Jasper", "Finch", "M"),
        ("Victor", "Okafor", "M"),
    ]

    students = []
    today = date.today()
    
    for first, last, gender in student_data:
        email = f"{first.lower()}.{last.lower()}@student.edu"
        user = User.objects.create_user(
            email=email, 
            password="password123", 
            role='student',
            first_name=first,
            last_name=last
        )
        
        # Generate age between exactly 14 and less than 17 years old
        # 14 years in days ~ 5113, 17 years in days ~ 6209
        days_old = random.randint(14 * 365 + 3, 17 * 365 + 4 - 1)  # Approximate leap years included
        dob = today - timedelta(days=days_old)
        
        student = Student.objects.create(
            email=email, 
            first_name=first, 
            last_name=last, 
            gender=gender,
            date_of_birth=dob
        )
        students.append(student)

    print("📚 Creating Enrollments...")
    
    # "Leave one student to offer only one subject"
    # We will pick Victor Okafor for this special rule.
    single_course_student = students[-1] 
    Enrollment.objects.create(
        student=single_course_student, 
        course=random.choice(all_courses)
    )

    # For the remaining students, enroll them in at least 2 courses, but randomize which ones.
    remaining_students = students[:-1]
    
    for student in remaining_students:
        # Randomize how many courses they take: between 2 and 5
        num_courses = random.randint(2, 5)
        # Randomly sample unique courses so they don't enroll in the same one twice
        enrolled_courses = random.sample(all_courses, num_courses)
        
        for c in enrolled_courses:
            Enrollment.objects.create(student=student, course=c)

    print("\n✅ Database Seeding Completed Successfully!")
    print(f"   Total Teachers: {Teacher.objects.count()}")
    print(f"   Total Courses: {Course.objects.count()}")
    print(f"   Total Students: {Student.objects.count()}")
    print(f"   Total Enrollments: {Enrollment.objects.count()}")
    print("\nUse password: 'password123' to log in via API for any generated user.")

if __name__ == '__main__':
    run()
