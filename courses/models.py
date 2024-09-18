from django.db import models
from django.contrib.auth.models import User
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class CourseType(models.Model):
    course_type=models.CharField(max_length=50)
    def __str__(self):
        return self.course_type

class Course(models.Model):
    course_type_id=models.ForeignKey(CourseType,on_delete=models.CASCADE)
    course_title=models.CharField(max_length=200)
    course_description=models.TextField()
    order=models.CharField(max_length=20)

    def __str__(self):
        return self.course_title
    
class Instructor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contact_address=models.TextField()
    call_num=models.CharField(max_length=40)

    def __str__(self):
        return self.user_registration_id

class Lesson(models.Model):
    course_id= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    instructor_id = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name='lessons')
   # title = models.CharField(max_length=200)
    lesson_content = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson_content
    
class resources(models.Model):
    lesson_id=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    resource_title=models.TextField()
    resource_link=models.TextField()

    def __str__(self):
        return self.resource_title
    
class Section(models.Model):
    lesson_id=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField()
    order=models.IntegerField()

    def __str__(self):
        return self.title

class LearningPath(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_paths')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    estimated_duration = models.IntegerField(help_text="Estimated duration in hours")
   
    def __str__(self):
        return self.title
    
class lesson_progress_tracker(models.Model):
    lesson_id=models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    last_accessed_timestamp=models.DateTimeField(null=True,blank=True)
    is_completed=models.BooleanField()
    learning_path_id=models.ForeignKey(LearningPath,on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return super().__str__()
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
    review_id=models.ForeignKey(Review, on_delete=models.CASCADE)
    instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    content=models.TextField()
    created_timestamp = models.DateTimeField(auto_now=True)

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_id =models.ForeignKey(Course,on_delete=models.CASCADE)
    Instructor_id = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class AssignmentSubmission(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assigment_content = models.TextField()
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    scores = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
     
    def __str__(self):
        return f"Submission for {self.assignment_id.title} by {self.user.first_name}"