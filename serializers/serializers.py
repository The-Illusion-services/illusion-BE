from datetime import timedelta
from accounts.models import *
from courses.models import *
from jobs.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'email', 'password', 'role']
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



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']

    def to_representation(self, instance):
        """Override to conditionally exclude the 'is_correct' field."""
        representation = super().to_representation(instance)
        
        # Check if the request is from an admin or the course creator
        request = self.context.get('request')
        if request and (request.user.is_staff or request.user == instance.question.quiz.module.course.created_by):
            # Expose 'is_correct' for admins or course creators
            return representation
        else:
            # Hide 'is_correct' for regular users
            representation.pop('is_correct', None)
            return representation

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']

    def get_fields(self):
        """Pass the request context to the AnswerSerializer."""
        fields = super().get_fields()
        request = self.context.get('request')
        fields['answers'].context.update({'request': request})
        return fields


class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'user', 'submitted_at', 'score']
    
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)


    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'created_at']

    def get_fields(self):
        """Pass the request context to the QuestionSerializer."""
        fields = super().get_fields()
        request = self.context.get('request')
        fields['questions'].context.update({'request': request})
        return fields
         



class LessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Allow id to be writable

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_resource', 'lesson_file','content', 'is_published']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)  # Include lessons in the module
    quizzes = QuizSerializer(many=True, required=False)
    class Meta:
        model = Module
        fields = ['id', 'title', 'lessons', 'quizzes']

    def validate_lessons(self, value):
        request_method = self.context['request'].method
        if request_method == 'PATCH':
            for lesson in value:
                if 'id' not in lesson:
                    raise serializers.ValidationError({"id": "This field is required for updating a lesson."})
        return value

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        module = Module.objects.create(**validated_data)  # Create the module

        for lesson_data in lessons_data:
            Lesson.objects.create(module=module, **lesson_data)  # Create lessons for this module

        return module
    
    """
    i will come back to this commented code in case for reference 
    purpose
    
    """
    def update(self, instance, validated_data):
        request_method = self.context['request'].method


        # Get the existing lessons
        existing_lessons = instance.lessons.all()

        # Process the incoming lessons data
        lessons_data = validated_data.pop('lessons', [])

        # Create a dictionary to store the updated lessons
        updated_lessons = {}

        if request_method == 'PATCH':
            for lesson_data in lessons_data:
                lesson_id = lesson_data.get('id')
                if not lesson_id:
                    raise serializers.ValidationError({"id": "This field is required for updating a lesson."})

                # Update an existing lesson
                lesson_instance = existing_lessons.filter(id=lesson_id).first()
                if lesson_instance:
                    for attr, value in lesson_data.items():
                        setattr(lesson_instance, attr, value)
                    updated_lessons[lesson_id] = lesson_instance
                else:
                    raise serializers.ValidationError({"id": f"Lesson with id {lesson_id} does not exist."})

        elif request_method == 'PUT':
            for lesson_data in lessons_data:
                lesson_id = lesson_data.get('id')
                if lesson_id:
                    # Update an existing lesson
                    lesson_instance = existing_lessons.filter(id=lesson_id).first()
                    if lesson_instance:
                        for attr, value in lesson_data.items():
                            setattr(lesson_instance, attr, value)
                        updated_lessons[lesson_id] = lesson_instance
                    else:
                        raise serializers.ValidationError({"id": f"Lesson with id {lesson_id} does not exist."})
                else:
                    # Create a new lesson
                    lesson_data['module'] = instance
                    new_lesson = Lesson(**lesson_data)
                    new_lesson.save()
                    updated_lessons[new_lesson.id] = new_lesson

        # Save updated lessons
        for lesson_id, lesson_instance in updated_lessons.items():
            lesson_instance.save()

        # Update the module fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField() 
    modules = ModuleSerializer(many=True, required=False)  # Include modules in the course

    class Meta:
        model = Course
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        fields = [
            'id', 'course_title', 'course_description', 
            'course_language', 'course_level', 'course_banner', 'course_category',
            'price', 'certification', 'estimated_duration', 'created_by',
            'created_at', 'updated_at', 'modules', 
        ]

    def create(self, validated_data):
            # Extract modules data from the validated data
            modules_data = validated_data.pop('modules', [])

            # Create the course
            course = Course.objects.create(**validated_data)

            # Create modules, lessons, quizzes, questions, and answers
            for module_data in modules_data:
                lessons_data = module_data.pop('lessons', [])
                quizzes_data = module_data.pop('quizzes', [])

                # Create the module
                module = Module.objects.create(course=course, **module_data)

                # Create lessons for the module
                for lesson_data in lessons_data:
                    Lesson.objects.create(module=module, **lesson_data)

                # Create quizzes for the module
                for quiz_data in quizzes_data:
                    questions_data = quiz_data.pop('questions', [])
                    quiz = Quiz.objects.create(module=module, **quiz_data)

                    # Create questions for the quiz
                    for question_data in questions_data:
                        answers_data = question_data.pop('answers', [])
                        question = Question.objects.create(quiz=quiz, **question_data)

                        # Create answers for the question
                        for answer_data in answers_data:
                            Answer.objects.create(question=question, **answer_data)

            return course
    
    def get_created_by(self, obj):
        """Return the first name and last name of the creator."""
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return None  


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




class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'lesson', 'module', 'resource_title', 'resource_link', 'file_upload']


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
