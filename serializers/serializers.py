from datetime import timedelta
from accounts.models import *
from courses.models import *
from jobs.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'company', 'last_name', 'phone', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
            'role': {'required': True},
           
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email')
        validated_data['username'] = email  # Use email as username
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class GoogleSignUpSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        from ..accounts.google import verify_google_token
        user_info = verify_google_token(token)
        if not user_info:
            raise serializers.ValidationError("Invalid or expired token")
        return user_info

    def create(self, validated_data):
        user_info = validated_data['token']
        email = user_info['email']
        name = user_info['name']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split('@')[0], "first_name": name}
        )

        return user





class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)  # Include lessons in the module

    class Meta:
        model = Module
        fields = ['title', 'lessons']

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        module = Module.objects.create(**validated_data)  # Create the module

        for lesson_data in lessons_data:
            Lesson.objects.create(module=module, **lesson_data)  # Create lessons for this module

        return module

    def update(self, instance, validated_data):
        # Pop out the lessons data from validated data
        lessons_data = validated_data.pop('lessons', [])

        # Update module fields
        instance = super().update(instance, validated_data)

        # Create a list of existing lesson IDs
        existing_lessons = instance.lessons.all()  # Get all lessons of the module
        existing_lessons_ids = [lesson.id for lesson in existing_lessons]

        # Process incoming lessons data
        for lesson_data in lessons_data:
            lesson_id = lesson_data.get('id', None)

            # Update existing lesson if it's in the module
            if lesson_id and lesson_id in existing_lessons_ids:
                lesson_instance = Lesson.objects.get(id=lesson_id, module=instance)
                LessonSerializer().update(lesson_instance, lesson_data)

            # If it's a new lesson (no ID), create it
            else:
                Lesson.objects.create(module=instance, **lesson_data)

    

        return instance


class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    modules = ModuleSerializer(many=True, required=False)  # Include modules in the course

    class Meta:
        model = Course
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        fields = '__all__'

    def create(self, validated_data):
        # Extract modules and lessons from validated data
        modules_data = validated_data.pop('modules', [])  # Extract modules data if any
        
        # Create the course first
        course = Course.objects.create(**validated_data)  # Save the course
        
        # Now, handle creating modules and lessons
        for module_data in modules_data:
            lessons_data = module_data.pop('lessons', [])  # Extract lessons if any
            
            # Create each module, associate it with the course
            module = Module.objects.create(course=course, **module_data)

            # Create lessons for each module if any lessons provided
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)

        return course


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Enrollment
        read_only_fields = ['user', 'enrollment_date']
        fields = ['user', 'course', 'enrollment_date']



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']



class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgressTracker
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'created_by', 'created_at']

class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'user', 'submitted_at', 'score']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'lesson', 'module', 'resource_title', 'resource_link']


class CertificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    course = serializers.ReadOnlyField(source='course.course_title')
    class Meta:
        model = Certification
        fields = ['id', 'user', 'course', 'issued_on', 'certificate_code', 'is_verified']
        read_only_fields = ['id', 'issued_on', 'certificate_code']





"""
Jobs creations and application sterializers
"""

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
    
    def validate_title(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Job title must be at least 8 characters long.")
        return value

    def validate_min_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Min Salary cannot be negative.")
        return value
    
    def validate_max_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Min Salary cannot be negative.")
        return value

    def validate(self, data):
        if 'job_descriptions' in data and 'title' in data:
            if data['job_descriptions'].lower() == data['title'].lower():
                raise serializers.ValidationError("Job description cannot be the same as the title.")
        return data

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('applicant', 'applied_at')

    def validate_cover_letter(self, value):
        if len(value) < 50:
            raise serializers.ValidationError("Cover letter must be at least 50 characters long.")
        return value

    def validate_resume(self, value):
        max_size = 3 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise serializers.ValidationError("Resume file size cannot exceed 3 MB.")
        return value

    def validate(self, data):
        if self.instance:  # This is an update
            if self.instance.applied_at < timezone.now() - timedelta(days=1):
                raise serializers.ValidationError("Applications cannot be edited after 24 hours.")
        
        if 'job' in data:
            existing_application = Application.objects.filter(
                job=data['job'],
                applicant=self.context['request'].user
            ).exists()
            if existing_application:
                raise serializers.ValidationError("You have already applied for this job.")
        
        return data