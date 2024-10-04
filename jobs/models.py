from django.db import models
from accounts.models import User

EXPERIENCE_LEVELS=[
    ('Senior','Senior'),
    ('Junior','Junior'),
    ('Intern','Intern'),
    ('Expert','Expert')
]

class Job(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    required_skills = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=200)
    job_descriptions=models.TextField()
    location = models.CharField(max_length=100)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('withdrawn', 'Withdrawn'),
    ]
    
class Application(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"