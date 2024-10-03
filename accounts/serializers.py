from .models import *
from rest_framework import serializers # type: ignore
from jobs.models import Job, Application
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'company', 'last_name', 'phone', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
            'role': {'required': False},
           
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
        from .google import verify_google_token
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'company', 'last_name', 'phone', 'email', 'role')
        read_only_fields = ('id',)
    

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