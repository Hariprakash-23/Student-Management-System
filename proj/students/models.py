from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')
    Reg_no = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=100)
    DOB = models.DateField()
    Address = models.TextField()
    Phone = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.Reg_no}-{self.Name}"
