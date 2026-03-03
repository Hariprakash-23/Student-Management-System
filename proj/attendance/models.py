from django.db import models
from students.models import Student
from courses.models import Course
# Create your models here.

class Attendance(models.Model):
    CHOICES = (
        ('present','Present'),
        ('absent','Absent')
    )
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendance')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10,choices=CHOICES,default='present')

    def __str__(self):
        return f"{self.student.Name} - {self.status}"
