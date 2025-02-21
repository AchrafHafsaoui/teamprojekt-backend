from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not sent in responses
        }

    def create(self, validated_data):
        # Use the manager's `create_user` to hash the password
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField() 
    password = serializers.CharField(write_only=True)