from django.contrib import admin
from .models import Student, Activity

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecturer', 'supervisor', 'grade')
    search_fields = ('user__username', 'lecturer__username', 'supervisor__username')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'activity', 'lesson_learned')
    search_fields = ('student__user__username', 'activity', 'lesson_learned')
    list_filter = ('date',)
