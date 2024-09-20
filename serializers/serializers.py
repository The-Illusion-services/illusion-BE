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




class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Course
        read_only_fields = ['id','created_by', 'created_at', 'updated_at']
        fields = '__all__'

