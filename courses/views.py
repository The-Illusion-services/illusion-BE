from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import PermissionDenied
# Create your views here.
from rest_framework import generics
from serializers.serializers import *
from permissions.permissions import IsEmployer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly



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
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



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
    permission_classes = [IsAuthenticatedOrReadOnly]

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
