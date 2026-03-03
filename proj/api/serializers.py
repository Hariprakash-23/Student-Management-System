from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student
from courses.models import Course
from attendance.models import Attendance
from marks.models import Marks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'