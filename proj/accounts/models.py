from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    Role_Choices = (
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role = models.CharField(max_length=10,choices=Role_Choices,default='student')
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username}-{self.role}"
