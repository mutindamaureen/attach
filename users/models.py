from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STUDENT = 'student'
    LECTURER = 'lecturer'
    SUPERVISOR = 'supervisor'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (LECTURER, 'Lecturer'),
        (SUPERVISOR, 'Supervisor'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
