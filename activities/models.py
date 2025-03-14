# from django.db import models
# from users.models import User
# from django.utils import timezone

# class Activity(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
#     date = models.DateField(default=timezone.now, unique_for_date="student")
#     description = models.TextField()
#     supervisor_comment = models.TextField(blank=True, null=True)
#     lecturer_comment = models.TextField(blank=True, null=True)
#     grade = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.student.username} - {self.date}"


from django.conf import settings
from django.db import models
from django.utils import timezone
# from users.models import User
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student")
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lecturer_students")
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="supervisor_students")
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Activity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="activities")
    date = models.DateField(default=timezone.now, unique_for_date="student")  # Auto set date when activity is created
    activity = models.TextField()  # Description of the student's activity
    lesson_learned = models.TextField()  # What the student learned from the activity
    supervisor_comment = models.TextField(null=True, blank=True)  # Supervisor's feedback
    lecturer_comment = models.TextField(null=True, blank=True)  # Lecturer's feedback

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"
