from django.db import models
from students.models import Student

class Parent(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    family_last_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        Student, 
        through='ParentStudent', 
        related_name='parents'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    linked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'student')
        db_table = 'parents_students'

    def __str__(self):
        return f"{self.parent} -> {self.student} ({self.relationship})"
