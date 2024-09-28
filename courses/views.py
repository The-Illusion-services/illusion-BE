from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import PermissionDenied
# Create your views here.
from rest_framework import generics
from serializers.serializers import *
from permissions.permissions import IsEmployee, IsEmployer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated



class CourseCreate(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Pass the request user to the serializer
        serializer.save(created_by=self.request.user)


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer




class ModuleCreateView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployer]

    def perform_create(self, serializer):
        # Get the course ID from the request data
        course_id = self.request.data.get('course')

        # Retrieve the course object
        course = get_object_or_404(Course, id=course_id)

        # Check if the current user is the one who created the course
        if course.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to create modules for this course.")

        # Save the module, associate it with the course, and set the user as the creator
        serializer.save(course=course)



class ModuleUpdateView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployer]

    def perform_update(self, serializer):
        # Get the module to update
        module = self.get_object()

        # Check if the user who created the course/module is the same user
        if module.course.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to update this module.")

        # Proceed with the update
        serializer.save()

class ModuleListView(generics.ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Module.objects.filter(course_id=course_id)




class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    


class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployer]

    def perform_create(self, serializer):
        # Get the course ID from the request data
        course_id = self.request.data.get('course')

        # Retrieve the course object
        course = get_object_or_404(Course, id=course_id)

        # Ensure the user creating the assignment is the course creator
        if course.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to create assignments for this course.")

        # Save the assignment and associate it with the course
        serializer.save(course=course, created_by=self.request.user)



class AssignmentUpdateView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployer]

    def perform_update(self, serializer):
        assignment = self.get_object()

        # Check if the user updating the assignment is the one who created it
        if assignment.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to update this assignment.")

        # Save the updated assignment
        serializer.save()


class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filter assignments by the course ID passed in the URL
        course_id = self.kwargs.get('course_id')
        return Assignment.objects.filter(course_id=course_id)



class EnrollCourseView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    def create(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=request.data.get('course'))
        user = request.user

        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(user=user, course=course).exists():
            raise ValidationError({"message": "You are already enrolled in this course."})

        # Proceed to create the enrollment
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, course=course)

        # Return custom success response
        response_data = {
            "message": "You have been enrolled successfully",
            "enrollment": serializer.data  # You can include the serialized data for more details
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Get the course based on the provided course_id in the URL
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        # Filter enrollments by the selected course
        return Enrollment.objects.filter(course=course)


class AssignmentSubmissionCreateView(generics.CreateAPIView):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    def perform_create(self, serializer):
        assignment = get_object_or_404(Assignment, id=self.request.data.get('assignment'))
        serializer.save(user=self.request.user, assignment=assignment)


class LessonProgressUpdateView(generics.UpdateAPIView):
    queryset = LessonProgressTracker.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def perform_update(self, serializer):
        progress = self.get_object()

        # Ensure only the owner can update the progress
        if progress.user != self.request.user:
            raise PermissionDenied("You cannot update someone else's progress.")

        serializer.save()


class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsEmployer]  # Ensure only employers can create quizzes

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

class QuizSubmissionView(generics.CreateAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, id=self.request.data.get('quiz'))
        user = self.request.user

        # Logic to calculate score based on user's answers
        submitted_answers = self.request.data.get('answers', [])
        correct_answers = 0
        total_questions = quiz.questions.count()

        for answer in submitted_answers:
            question_id = answer.get('question_id')
            selected_answer_id = answer.get('answer_id')
            correct_answer = Answer.objects.filter(question_id=question_id, is_correct=True).first()

            if correct_answer and correct_answer.id == selected_answer_id:
                correct_answers += 1

        # Calculate score as a percentage
        score = (correct_answers / total_questions) * 100

        # Save the submission
        serializer.save(user=user, quiz=quiz, score=score)


class ResourceListView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson', None)
        module_id = self.request.query_params.get('module', None)

        if lesson_id:
            return Resource.objects.filter(lesson_id=lesson_id)
        elif module_id:
            return Resource.objects.filter(module_id=module_id)
        return Resource.objects.none()

class ResourceCreateView(generics.CreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        lesson_id = self.request.data.get('lesson')
        module_id = self.request.data.get('module')

        if lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id)

            # Ensure the lesson creator (via module) is the same as the request user
            if lesson.module.course.created_by != self.request.user:
                raise PermissionDenied("Only the employer who created the lesson can add resources.")

            serializer.save(lesson=lesson)
        
        elif module_id:
            module = get_object_or_404(Module, id=module_id)

            # Ensure the module creator is the same as the request user
            if module.course.created_by != self.request.user:
                raise PermissionDenied("Only the employer who created the module can add resources.")

            serializer.save(module=module)

class CertificationListCreateView(generics.ListCreateAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned certifications to the current user.
        """
        return Certification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the user as the owner of the certification when creating.
        """
        serializer.save(user=self.request.user)


# Retrieve, update a certification
class CertificationDetailView(generics.RetrieveAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the queryset to only allow users to access their own certifications.
        """
        return Certification.objects.filter(user=self.request.user)