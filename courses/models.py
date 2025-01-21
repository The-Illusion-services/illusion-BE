import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

class Course(models.Model):
    course_title = models.CharField(max_length=200)
    course_description = models.TextField()
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    course_video = models.FileField(upload_to='course_videos/', blank=True, null=True)
    course_banner = models.ImageField(upload_to='course_banners/', blank=True, null=True)

    course_language = models.CharField(max_length=50, default='English')
    
    
    course_level = models.CharField(
        max_length=50, 
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Web3 Expert', 'Web3 Expert')],
        default='Beginner'
    )
    
    # Web3-specific topics or categories
    course_category = models.CharField(
        max_length=100, 
        choices=[
            ('Blockchain Basics', 'Blockchain Basics'),
            ('Smart Contracts', 'Smart Contracts'),
            ('dApp Development', 'dApp Development'),
            ('Decentralized Governance', 'Decentralized Governance'),
            ('Crypto Wallets', 'Crypto Wallets'),
            ('NFTs', 'NFTs'),
            ('DeFi', 'DeFi'),
        ], default=''
    )

    
    price = models.DecimalField(max_digits=8, decimal_places=2, default='')  # Adjust max_digits as needed
    
   
    certification = models.BooleanField(default=False)

    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_duration = models.IntegerField(help_text="Estimated duration in hours", default=1)
    
    # Tracking creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_title} - {self.created_by}"

class Module(models.Model):
    title=models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.title
    
    
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, related_name='lessons')
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default="")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} Lesson - from {self.module.course.course_title} - created by {self.module.course.created_by.username}- created at {self.module.course.created_at}"

class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources", null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="resources", null=True, blank=True)
    resource_title = models.CharField(max_length=255)
    resource_link = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to='resource_files/', blank=True, null=True)



    def __str__(self):
        return f"Resource: {self.resource_title}"

    
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments',default="")
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments',default="")
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews',default=None)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.course.course_title}"

    class Meta:
        unique_together = ['user', 'course']  # Ensure one review per user per course
        
class ReviewResponse(models.Model):
    review = models.ForeignKey(Review, default="", on_delete=models.CASCADE,)
    content=models.TextField()
    created_timestamp = models.DateTimeField(auto_now=True)


    
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions',default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions',default="")
    assigment_content = models.TextField()
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    scores = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
     
    def __str__(self):
        return f"Submission for {self.assignment_id.title} by {self.user.first_name}"
    

class LessonProgressTracker(models.Model):
    user = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, default=False, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_accessed_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.lesson.title}"






class Quiz(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, default=False, on_delete=models.CASCADE, related_name="quizzes")
    created_by = models.ForeignKey(User, default=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz: {self.title} for {self.course.course_title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()

    def __str__(self):
        return f"Question: {self.question_text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.answer_text} (Correct: {self.is_correct})"

class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"Submission by {self.user.username} for Quiz {self.quiz.title}"




class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='certifications')
    issued_on = models.DateTimeField(default=timezone.now)
    certificate_code = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Certification for {self.user.username} - {self.course.course_title}"

    def generate_certificate_code(self):
        """
        Generates a unique certificate code, this can be customized as needed.
        """
        self.certificate_code = uuid.uuid4().hex[:10].upper()

    def save(self, *args, **kwargs):
        # Generate certificate code before saving if not set
        if not self.certificate_code:
            self.generate_certificate_code()
        super().save(*args, **kwargs)
