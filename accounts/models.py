from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


ROLE_CHOICES = [
   ( 'Employee', 'Employee'),
   ('Employer', 'Employer'),
   
]

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=200, default='')
    role = models.CharField(max_length=200, choices=ROLE_CHOICES)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.email} - {self.first_name} - {self.role}"


    
class ValidationTrack(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    validation_code=models.IntegerField()
    is_validated=models.BooleanField()

    def __str__(self):
        return self.validation_code


    
