import datetime

from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

class UserCategory(models.Model):
    user_category=models.CharField(max_length=150)
    def __str__(self):
        return self.user_category

class Field(models.Model):
    field=models.CharField(max_length=150)
    description=models.TextField()
    def __str__(self):
        return self.field

class UserRegistration(models.Model):
    last_name=models.CharField(max_length=50)
    first_name = models.CharField(max_length=80)
    field_id=models.ForeignKey("Field",on_delete=models.CASCADE)
    user_category_id=models.ForeignKey("UserCategory", on_delete=models.CASCADE)
    email=models.CharField(max_length=250)

    def __str__(self):
        return self.email


class UserLoginDetails(models.Model):
    username=models.CharField(max_length=50)
    pw=models.CharField(max_length=250)
    user_registration_id=models.ForeignKey('UserRegistration',on_delete=models.CASCADE)
    last_login_timestamp = models.DateTimeField("last login time")
    last_logout_timestamp = models.DateTimeField("last logout time")
    login_ip = models.CharField(max_length=50)
    user_status = models.CharField(max_length=10)
    
    def __str__(self):
        return self.username

class ValidationTrack(models.Model):
    user_registraton_id=models.ForeignKey("UserRegistration",on_delete=models.CASCADE)
    validation_code=models.IntegerField(max_length=10)
    is_validated=models.BooleanField()

    def __str__(self):
        return self.validation_code

class CourseType(models.Model):
    course_type=models.CharField(max_length=50)
    def __str__(self):
        return self.course_type

class Course(models.Model):
    course_type_id=models.ForeignKey("CourseType",on_delete=models.CASCADE)
    course_title=models.CharField(max_length=200)
    course_description=models.TextField()
    order=models.CharField(max_length=20)

    def __str__(self):
        return self.course_title

class QuestionType(models.Model):
    question_type=models.CharField(max_length=50)

    def __str__(self):
        return self.question_type
    
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_by_user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", null=True, blank=True)
    pass_score = models.FloatField(help_text="Minimum score to pass the quiz (percentage)")
    is_active = models.BooleanField(default=True)
   # shuffle_questions = models.BooleanField(default=False)
    #max_attempts = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"
    



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
"""
to be used later 
class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"
"""
class UserAnswer(models.Model):
    #attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.attempt.user.username}"
    
class Instructor(models.Model):
    user_registration_id=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
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
    order=models.IntegerField(max_length=10)

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
    user_registration_id=models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    last_accessed_timestamp=models.DateTimeField(null=True,blank=True)
    is_completed=models.BooleanField()
    learning_path_id=models.ForeignKey(LearningPath,on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return super().__str__()

class SettingCategory(models.Model):
    setting_name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.setting_name

class Setting(models.Model):
    category_id = models.ForeignKey(SettingCategory, on_delete=models.CASCADE, related_name='settings')
    #key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data_type = models.CharField(max_length=20, choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ])
    default_value = models.TextField()

    def __str__(self):
        return self.name



class SystemSetting(models.Model):
    setting = models.ForeignKey('Setting', on_delete=models.CASCADE, related_name='system_settings')
    value = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    updated_by_user_id = models.ForeignKey(UserRegistration, on_delete=models.SET_NULL, null=True)
    is_override = models.BooleanField(default=True)

    class Meta:
        unique_together = ['setting']

    def __str__(self):
        return f"{self.setting.key}: {self.value}"

    def save(self, *args, **kwargs):
        # Custom logic to validate value based on setting.data_type
        # For example:
        if self.setting.data_type == 'integer':
            self.value = int(self.value)
        elif self.setting.data_type == 'boolean':
            self.value = str(bool(self.value)).lower()
        super().save(*args, **kwargs)


class UserSetting(models.Model):
    user = models.OneToOneField(UserRegistration, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=20, default='light')
    notifications_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    daily_email_digest=models.BooleanField(default=False)
    privacy_level =models.IntegerField(max_length=3,default=0,db_comment="0 for private and 1 for public")

    def __str__(self):
        return f"{self.user.username}'s settings"

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
    user_registration_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='submissions')
    assigment_content = models.TextField()
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    scores = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
     
    def __str__(self):
        return f"Submission for {self.assignment_id.title} by {self.user_registration_id.first_name}"


class Review(models.Model):
    user_registration_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user_registration_id.first_name} for {self.course.course_title}"

    class Meta:
        unique_together = ['user_registration_id', 'course']  # Ensure one review per user per course
class ReviewResponse(models.Model):
    review_id=models.ForeignKey(Review, on_delete=models.CASCADE)
    instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    content=models.TextField()
    created_timestamp = models.DateTimeField(auto_now=True)