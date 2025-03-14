from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ActivitySerializer, SupervisorCommentSerializer, StudentSerializer, LecturerCommentSerializer, GradeSerializer, Activity1Serializer
from .models import Student, Activity
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework.views import APIView
import logging
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import date


logger = logging.getLogger(__name__)

class LecturerStudentListView(generics.ListAPIView):
    """
    List all students assigned to the logged-in lecturer.
    """
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(lecturer=self.request.user)

class LecturerStudentActivitiesView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Activity.objects.filter(student__id=student_id, student__lecturer=self.request.user).order_by('-date')

class LecturerCommentView(generics.UpdateAPIView):
    serializer_class = LecturerCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Ensure the lecturer is modifying an activity belonging to an assigned student."""
        activity = get_object_or_404(Activity, id=self.kwargs['pk'])

        # Ensure only the assigned lecturer can comment
        if activity.student.lecturer != self.request.user:
            raise PermissionDenied("You are not allowed to comment on this activity.")

        return activity

    def update(self, request, *args, **kwargs):
        """Allow lecturer to update only the lecturer_comment field."""
        activity = self.get_object()
        serializer = self.get_serializer(activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Comment added successfully!",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)


class LecturerGradeView(generics.UpdateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        student = get_object_or_404(Student, id=kwargs['student_id'], lecturer=request.user)

        serializer = self.get_serializer(student, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Grade submitted successfully!", "data": serializer.data})
        
        return Response(serializer.errors, status=400)


class SupervisorStudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(supervisor=self.request.user)


class SupervisorActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(student__supervisor=self.request.user).order_by('-date')


logger = logging.getLogger(__name__)

class SupervisorCommentView(generics.UpdateAPIView):
    serializer_class = SupervisorCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        logger.info("PATCH request received for activity ID %s", kwargs["pk"])
        logger.info("Request data: %s", request.data)

        activity = get_object_or_404(Activity, id=kwargs['pk'], student__supervisor=request.user)

        serializer = self.get_serializer(activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info("Comment successfully saved for activity ID %s", activity.id)
            return JsonResponse({"message": "Comment added successfully!", "data": serializer.data})

        logger.error("Validation failed: %s", serializer.errors)
        return JsonResponse(serializer.errors, status=400)


class SupervisorStudentActivitiesView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Activity.objects.filter(student__id=student_id, student__supervisor=self.request.user).order_by('-date')



class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve only the activities of the logged-in student"""
        if hasattr(self.request.user, "student"):
            return Activity.objects.filter(student=self.request.user.student).order_by('-date')
        return Activity.objects.none()

    def perform_create(self, serializer):
        """Ensure students cannot submit multiple entries for the same day"""
        student = self.request.user.student
        today = date.today()

        # Check if an activity already exists for today
        if Activity.objects.filter(student=student, date=today).exists():
            raise ValidationError({"error": "You have already submitted an activity for today."})

        # Set student and date automatically
        serializer.save(student=student, date=today)
