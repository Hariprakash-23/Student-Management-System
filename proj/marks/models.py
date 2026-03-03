from django.db import models
from courses.models import Course
from students.models import Student

class Exam(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    max_marks = models.IntegerField()

    def __str__(self):
        return f"{self.course.code} - {self.name}"

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.exam.name}: {self.marks_obtained}"