from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from serializers.serializers import *
from permissions.permissions import IsEmployer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class CourseListAndCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployer]

    def perform_create(self, serializer):
        # Pass the request user to the serializer
        serializer.save(created_by=self.request.user)
