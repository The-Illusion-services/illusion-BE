from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

import uuid


ROLE_CHOICES = [
   ( 'Learner', 'Learner'),
   ('Creator', 'Creator'),
   
]

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default="Learner")
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
     # Avoid clashes with Django's built-in Group and Permission models
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    

    def __str__(self):
        return f"{self.email} - {self.first_name} - {self.role}"


    
class ValidationTrack(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    validation_code=models.IntegerField()
    is_validated=models.BooleanField()

    def __str__(self):
        return self.validation_code


    
