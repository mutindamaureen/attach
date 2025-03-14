
from django.urls import path
from .views import (
    LecturerStudentListView,
    LecturerStudentActivitiesView,
    LecturerCommentView,
    LecturerGradeView,
    SupervisorActivityListView,
    SupervisorCommentView,
    ActivityListCreateView,
    SupervisorStudentActivitiesView,
    SupervisorStudentListView
)

urlpatterns = [
    # Lecturer Endpoints
    path('lecturer/students/', LecturerStudentListView.as_view(), name='lecturer-students'),
    path('lecturer/students/<int:student_id>/activities/', LecturerStudentActivitiesView.as_view(), name='lecturer-student-activities'),
    path('lecturer/comment/<int:pk>/', LecturerCommentView.as_view(), name='lecturer-comment'),
    path('lecturer/grade/<int:student_id>/', LecturerGradeView.as_view(), name='lecturer-grade'),

    # Supervisor Endpoints
    path('supervisor/activities/', SupervisorActivityListView.as_view(), name='supervisor-activities'),
    path('supervisor/comment/<int:pk>/', SupervisorCommentView.as_view(), name='supervisor-comment'),
    path("supervisor/students/", SupervisorStudentListView.as_view(), name="supervisor-students"),
    # path("supervisor/students/<int:student_id>/activities/", StudentActivitiesView.as_view(), name="student-activities"),
    path("supervisor/students/<int:student_id>/activities/", SupervisorStudentActivitiesView.as_view(), name="student-activities"),



    # Student Endpoints
    path('activities/', ActivityListCreateView.as_view(), name='student-activities'),
    
]
