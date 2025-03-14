from rest_framework import serializers
from .models import Student, Activity

class Activity1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['student', 'date'] 

class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'grade']


class ActivitySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    # date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'student_name', 'activity', 'lesson_learned', 'supervisor_comment', 'lecturer_comment']
        read_only_fields = ['date', 'student', 'supervisor_comment', 'lecturer_comment']

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            raise serializers.ValidationError({"error": "User context is missing."})

        if not hasattr(request.user, "student"):
            raise serializers.ValidationError({"error": "Only students can submit activities."})

        validated_data["student"] = request.user.student  
        # validated_data["date"] = date.today()  # Automatically set the date

        return super().create(validated_data)


class LecturerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['lecturer_comment']

class SupervisorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['supervisor_comment']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['grade']

    def update(self, instance, validated_data):
        instance.grade = validated_data.get("grade", instance.grade)
        instance.save()
        return instance