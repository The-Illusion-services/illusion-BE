from .models import *
from rest_framework import serializers

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
