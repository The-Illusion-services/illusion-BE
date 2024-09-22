from django.db import models
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
    # course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')


    def __str__(self):
        return self.title
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, related_name='lessons')
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} Lesson - from {self.course} - created by {self.course}"

class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources", null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="resources", null=True, blank=True)
    resource_title = models.CharField(max_length=255)
    resource_link = models.URLField()

    def __str__(self):
        return f"Resource: {self.resource_title}"

    
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')
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
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content=models.TextField()
    created_timestamp = models.DateTimeField(auto_now=True)


    
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assigment_content = models.TextField()
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    scores = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
     
    def __str__(self):
        return f"Submission for {self.assignment_id.title} by {self.user.first_name}"
    

class LessonProgressTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_accessed_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.lesson.title}"






class Quiz(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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
