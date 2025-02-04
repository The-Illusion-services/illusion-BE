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
        read_only_fields = ['score']  



class QuizSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=serializers.DictField(),
        required=False  # Options are not mandatory
    )

    has_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'options', 'created_at', 'has_submitted']


    def get_has_submitted(self, obj):
        """Check if the user has submitted this quiz"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return QuizSubmission.objects.filter(quiz=obj, user=request.user).exists()
        return False

    def to_representation(self, instance):
        """Transform the response to include options."""
        representation = super().to_representation(instance)
        representation['options'] = [
            {
                "id": answer.id,
                "text": answer.answer_text,
                # "is_correct": answer.is_correct
            }
            for question in instance.questions.all()
            for answer in question.answers.all()
        ]
        return representation
    

    
    def create(self, validated_data):
        """Create a quiz along with nested questions and answers."""
        options = validated_data.pop('options', [])
        quiz = Quiz.objects.create(**validated_data)

        # Create a single question with the provided options
        question = Question.objects.create(quiz=quiz, question_text="Default Question")
        for option in options:
            Answer.objects.create(
                question=question,
                answer_text=option['text'],
                is_correct=option.get('isCorrect', False),
            )

        return quiz



class LessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Allow id to be writable

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_resource', 'lesson_file','content', 'is_published']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)
    quizzes = QuizSerializer(many=True, required=False)  # Use the updated QuizSerializer

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
        quizzes_data = validated_data.pop('quizzes', [])
        module = Module.objects.create(**validated_data)

        for lesson_data in lessons_data:
            Lesson.objects.create(module=module, **lesson_data)

        for quiz_data in quizzes_data:
            questions_data = quiz_data.pop('questions', [])
            quiz = Quiz.objects.create(module=module, **quiz_data)

            for question_data in questions_data:
                answers_data = question_data.pop('answers', [])
                question = Question.objects.create(quiz=quiz, **question_data)

                for answer_data in answers_data:
                    Answer.objects.create(question=question, **answer_data)

        return module

    def update(self, instance, validated_data):
        """ Update a module, its lessons, and quizzes """
        lessons_data = validated_data.pop('lessons', [])
        quizzes_data = validated_data.pop('quizzes', [])

        # Update module fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # ---- Updating Lessons ---- #
        existing_lessons = {lesson.id: lesson for lesson in instance.lessons.all()}
        for lesson_data in lessons_data:
            lesson_id = lesson_data.get('id')

            if lesson_id in existing_lessons:
                lesson_instance = existing_lessons[lesson_id]
                for attr, value in lesson_data.items():
                    setattr(lesson_instance, attr, value)
                lesson_instance.save()
            else:
                raise serializers.ValidationError({"id": f"Lesson with id {lesson_id} does not exist."})

        # ---- Updating Quizzes ---- #
        existing_quizzes = {quiz.id: quiz for quiz in instance.quizzes.all()}
        for quiz_data in quizzes_data:
            quiz_id = quiz_data.get('id')

            if quiz_id in existing_quizzes:
                quiz_instance = existing_quizzes[quiz_id]

                # Update quiz fields
                for attr, value in quiz_data.items():
                    if attr != 'options':  # Exclude options from direct update
                        setattr(quiz_instance, attr, value)
                quiz_instance.save()

                # ---- Updating Options ---- #
                existing_options = {answer.id: answer for question in quiz_instance.questions.all() for answer in question.answers.all()}
                for option in quiz_data.get('options', []):
                    option_id = option.get('id')

                    if option_id in existing_options:
                        option_instance = existing_options[option_id]
                        for attr, value in option.items():
                            setattr(option_instance, attr, value)
                        option_instance.save()
                    else:
                        raise serializers.ValidationError({"id": f"Option with id {option_id} does not exist."})

            else:
                raise serializers.ValidationError({"id": f"Quiz with id {quiz_id} does not exist."})

        return instance



class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    modules = ModuleSerializer(many=True, required=False)

    class Meta:
        model = Course
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        fields = [
            'id', 'course_title', 'course_description', 'course_language', 'course_level',
            'course_banner', 'course_category', 'price', 'certification', 'estimated_duration',
            'created_by', 'created_at', 'updated_at', 'modules',
        ]

    def create(self, validated_data):
        modules_data = validated_data.pop('modules', [])
        course = Course.objects.create(**validated_data)

        for module_data in modules_data:
            lessons_data = module_data.pop('lessons', [])
            quizzes_data = module_data.pop('quizzes', [])

            module = Module.objects.create(course=course, **module_data)

            # Create lessons for the module
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)

            # Create quizzes for the module
            for quiz_data in quizzes_data:
                quiz_serializer = QuizSerializer(data=quiz_data, context=self.context)
                quiz_serializer.is_valid(raise_exception=True)
                quiz_serializer.save(module=module)  # Save the quiz with the module

        return course

    def get_created_by(self, obj):
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
