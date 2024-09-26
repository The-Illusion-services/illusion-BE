from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from serializers.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import PermissionDenied
import uuid
import jwt
from django.conf import settings
import datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate, login




class UserRegistrationView(APIView):
    """
    API view to handle the registration of a new user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        
        data = request.data
        if data['password'] != data['confirm_password']:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password'],
            'company':data['company'],
            'role': data['role']
        })

        if serializer.is_valid():
            user = serializer.save()
            user.save()

            response_data = {
                'access_token': str(AccessToken.for_user(user)),
                'refresh_token': str(RefreshToken.for_user(user)),
                'message': 'Account Creation Successful'
            }

            

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = [AllowAny]



    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        
        # response data
        response_data = {
            'access_token': str(AccessToken.for_user(user)),
            'refresh_token': str(RefreshToken.for_user(user)),
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
        }

        

        return Response(response_data, status=status.HTTP_200_OK)



class GoogleSignUpView(APIView):
    def post(self, request):
        serializer = GoogleSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated"}, status=200)
