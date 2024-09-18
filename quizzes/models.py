from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from accounts.models import User

# Create your models here.

class QuestionType(models.Model):
    question_type=models.CharField(max_length=50)

    def __str__(self):
        return self.question_type
    
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.attempt.user.username}"
    