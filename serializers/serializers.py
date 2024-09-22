from accounts.models import *
from courses.models import *
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
        fields = '__all__'

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

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'



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
