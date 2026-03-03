from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from students.models import Student
from courses.models import Course
from attendance.models import Attendance
from marks.models import Marks
from .serializers import (
    UserSerializer, StudentSerializer, CourseSerializer,
    AttendanceSerializer, MarkSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarkSerializer