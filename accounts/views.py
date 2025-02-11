from django.shortcuts import render
from django.views import View
from accounts.serializers import ProfileSerializer
from permissions import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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
from django.core.mail import send_mail
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from urllib.parse import urljoin
import requests
from django.urls import reverse




class UserRegistrationView(APIView):
    """
    API view to handle the registration of a new user.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm Password'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['Employee', 'Employer'], description='Role'),
            },
            required=['first_name', 'last_name', 'email', 'password', 'confirm_password', 'role'],
        ),
        responses={201: 'Account Created', 400: 'Error'}
    )
    def post(self, request):
        data = request.data

        # Check if password and confirm password match
        if data['password'] != data.get('confirm_password'):
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the data for user creation
        serializer = UserSerializer(data={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password'],
            'role': data['role']
        })

        # Validate and save user
        if serializer.is_valid():
            user = serializer.save()

            send_mail(
                    'Welcome to Illusion Academy',
                    f'Dear {user.first_name}, welcome to Illusion Academy...',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

            # Generate tokens for the user
            response_data = {
                'access_token': str(AccessToken.for_user(user)),
                'refresh_token': str(RefreshToken.for_user(user)),
                'message': 'Account Creation Successful'
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Return errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'password'],
        ),
        responses={200: 'Token', 400: 'Error'}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Use Django's built-in authenticate function
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens and return response data
        response_data = {
            'access_token': str(AccessToken.for_user(user)),
            'refresh_token': str(RefreshToken.for_user(user)),
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for an access token
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": "http://localhost:5555/auth/callback",  # Must match the registered redirect URI
            "grant_type": "authorization_code",
        }

        token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
        token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
        print("Token Response Status:", token_response.status_code)
        print("Token Response Data:", token_response.json())  # Debugging log


        if token_response.status_code != 200:
            return Response(
                {"error": "Failed to exchange token", "details": token_response.json()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = token_response.json().get("access_token")

        # Fetch user details from Google
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code != 200:
            return Response(
                {"error": "Failed to fetch user details from Google", "details": user_info_response.json()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_data = user_info_response.json()
        email = user_data.get("email")
        first_name = user_data.get("given_name", "")
        last_name = user_data.get("family_name", "")

        if not email:
            return Response({"error": "Email not found in Google response"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists, if not create a new one
        user, created = User.objects.get_or_create(
            email=email,
            username=email,
            defaults={"first_name": first_name, "last_name": last_name, "role": "Learner"},
        )

        if not created:
            user.first_name = user.first_name or first_name
            user.last_name = user.last_name or last_name
            user.save()

        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


#     def get(self, request, *args, **kwargs):
#         code = request.GET.get("code")

#         if code is None:
#             return Response({"error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)

#         # Exchange the authorization code for an access token
#         token_data = {
#             "code": code,
#             "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
#             "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
#             "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
#             "grant_type": "authorization_code",
#         }

#         token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
#         print("Token Response:", token_response.json())  # Debugging log

#         if token_response.status_code != 200:
#             return Response(
#                 {"error": "Failed to exchange token", "details": token_response.json()},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         access_token = token_response.json().get("access_token")
#         if not access_token:
#             return Response({"error": "Access token missing"}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch user details from Google
#         user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
#         headers = {"Authorization": f"Bearer {access_token}"}
#         user_info_response = requests.get(user_info_url, headers=headers)

#         print("Google User Info Response:", user_info_response.json())  # Debugging log

#         if user_info_response.status_code != 200:
#             return Response(
#                 {"error": "Failed to fetch user details from Google", "details": user_info_response.json()},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user_data = user_info_response.json()
#         email = user_data.get("email")
#         first_name = user_data.get("given_name", "")
#         last_name = user_data.get("family_name", "")

#         if not email:
#             return Response({"error": "Email not found in Google response"}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if user exists, if not create a new one
#         user, created = User.objects.get_or_create(
#             email=email,
#             username=email,
#             defaults={"first_name": first_name, "last_name": last_name, "role": "Learner"},
#         )

#         if not created:
#             # Update missing fields if necessary
#             user.first_name = user.first_name or first_name
#             user.last_name = user.last_name or last_name
#             user.save()

#         # Generate access and refresh tokens
#         from rest_framework_simplejwt.tokens import RefreshToken

#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             "access_token": str(refresh.access_token),
#             "refresh_token": str(refresh),
#             "user_id": user.id,
#             "email": user.email,
#             "role": user.role,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)




# for testing the oauth flow
class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )


    

class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, id=None):
        if id:
            return User.objects.get(id=id)
        return self.request.user  # If no id is given, return the authenticated user

    def get(self, request, id=None):
        try:
            instance = self.get_object(id)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(kwargs.get('id'))
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [APIView]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()