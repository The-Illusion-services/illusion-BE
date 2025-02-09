from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import PermissionDenied
# Create your views here.
from rest_framework import generics
from serializers.serializers import *
from permissions.permissions import IsLearner, IsCreator 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.db.models import Count, Q, F, Sum
from rest_framework.views import APIView
from django.core.cache import cache
from .pagination import CustomPageNumberPagination



class CourseCreate(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreator]

    def perform_create(self, serializer):
        # Pass the request user to the serializer
        serializer.save(created_by=self.request.user)

class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def perform_update(self, serializer):
        course = self.get_object()

        # Check if the user updating the course is the one who created it
        if course.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to update this course.")

        # Proceed with the update
        serializer.save()


class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def perform_destroy(self, instance):
        # Check if the user deleting the course is the one who created it
        if instance.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to delete this course.")

        # Proceed with the deletion
        instance.delete()




class AvailableCoursesList(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination  

    def get_queryset(self):
        cache_key = "available_courses"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data  # Return cached results

        queryset = Course.objects.filter(is_deleted=False).select_related("created_by").order_by("-created_at")
        cache.set(cache_key, queryset, timeout=300)  # Cache for 5 minutes
        return queryset



class UserCreatedCoursesList(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination  

    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user, is_deleted=False).select_related("created_by").order_by("-created_at")



class UserEnrolledCoursesList(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination  

    def get_queryset(self):
        return Course.objects.filter(enrollments__user=self.request.user, is_deleted=False).select_related("created_by").order_by("-created_at")





class ModuleCreateView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreator]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreator]
    

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
        # Return all modules without any filtering
        return Module.objects.all()




class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    


class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreator]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreator]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsLearner]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsLearner]

    def perform_create(self, serializer):
        assignment = get_object_or_404(Assignment, id=self.request.data.get('assignment'))
        serializer.save(user=self.request.user, assignment=assignment)


class LessonProgressUpdateView(generics.UpdateAPIView):
    queryset = LessonProgressTracker.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, IsLearner]

    def perform_update(self, serializer):
        progress = self.get_object()

        # Ensure only the owner can update the progress
        if progress.user != self.request.user:
            raise PermissionDenied("You cannot update someone else's progress.")

        serializer.save()


class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsCreator]  # Ensure only Creators can create quizzes

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
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        module_id = request.data.get('module')  # Get the module ID from request
        quizzes_data = request.data.get('quizzes', [])  # List of quizzes with answers

        if not module_id or not quizzes_data:
            return Response({"error": "Module ID and quizzes data are required"}, status=status.HTTP_400_BAD_REQUEST)

        module = get_object_or_404(Module, id=module_id)

        # Ensure all quizzes belong to the same module
        quizzes = Quiz.objects.filter(module=module)
        if not quizzes.exists():
            return Response({"error": "No quizzes found for this module"}, status=status.HTTP_400_BAD_REQUEST)

        submissions = []
        for quiz_data in quizzes_data:
            quiz = get_object_or_404(Quiz, id=quiz_data['quiz'])
            submitted_answers = quiz_data.get('answers', [])

            correct_answers = 0
            total_questions = quiz.questions.count()

            for answer in submitted_answers:
                question = get_object_or_404(Question, id=answer['question_id'])
                selected_answer = get_object_or_404(Answer, id=answer['selected_answer_id'])
                if selected_answer.is_correct:
                    correct_answers += 1

            score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

            # Save submission
            submission, _ = QuizSubmission.objects.get_or_create(
                user=user, quiz=quiz, defaults={'score': score}
            )
            submissions.append(QuizSubmissionSerializer(submission).data)

        # Check if all quizzes in the module are completed
        all_quizzes_in_module = quizzes.count()
        completed_quizzes = QuizSubmission.objects.filter(user=user, quiz__module=module).count()

        next_module = Module.objects.filter(course=module.course, id__gt=module.id).order_by('id').first()
        next_module_unlocked = False

        if completed_quizzes == all_quizzes_in_module:
            if next_module:
                next_module_unlocked = True  # Indicate that the next module is unlocked
            else:
                # If no more modules, check for certification
                all_modules = Module.objects.filter(course=module.course).count()
                completed_modules = Module.objects.filter(
                    quizzes__quizsubmission__user=user
                ).distinct().count()

                if completed_modules == all_modules and not Certification.objects.filter(user=user, course=module.course).exists():
                    Certification.objects.create(user=user, course=module.course, is_verified=True)

        # Prepare response
        return Response({
            'quiz_submissions': submissions,
            'next_module_unlocked': next_module_unlocked,
            'certificate': CertificationSerializer(Certification.objects.filter(user=user, course=module.course).first()).data if next_module is None else None,
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })


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
    permission_classes = [IsAuthenticated, IsCreator]

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



class LearningProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        response_data = {}

        # Check if the user is a Creator
        is_creator = user.role == "Creator"

        if is_creator:
            # Creator Metrics (Filter out deleted courses)
            response_data["total_courses_created"] = Course.objects.filter(
                created_by=user, is_deleted=False
            ).count()

            response_data["total_enrollments"] = Enrollment.objects.filter(
                course__created_by=user, course__is_deleted=False
            ).count()

            response_data["total_revenue"] = Enrollment.objects.filter(
                course__created_by=user, course__is_deleted=False
            ).aggregate(revenue=Sum("course__price"))["revenue"] or 0
        else:
            # Learner Metrics
            response_data["total_courses_enrolled"] = Enrollment.objects.filter(
                user=user, course__is_deleted=False
            ).count()

            response_data["total_courses_completed"] = Certification.objects.filter(
                user=user, is_verified=True, course__is_deleted=False
            ).count()

            response_data["leaderboard_xp"] = QuizSubmission.objects.filter(
                user=user
            ).aggregate(total_xp=Sum("score"))["total_xp"] or 0

            # Count completed modules (Filter out deleted courses)
            total_modules_completed = Module.objects.filter(course__is_deleted=False).annotate(
                total_quizzes=Count("quizzes"),
                completed_quizzes=Count("quizzes", filter=Q(quizzes__quizsubmission__user=user))
            ).filter(total_quizzes=F("completed_quizzes")).count()

            response_data["total_modules_completed"] = total_modules_completed

        return Response(response_data)
