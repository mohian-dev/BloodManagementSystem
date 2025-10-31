from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import DonorProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_donor', 'is_admin']
        read_only_fields = ['is_donor', 'is_admin']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_donor=True
        )
        return user

class DonorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = DonorProfile
        fields = ['id', 'user', 'username', 'email', 'full_name', 'age', 'phone', 
                  'blood_group', 'location', 'is_available', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def validate_blood_group(self, value):
        valid_groups = [bg[0] for bg in BLOOD_GROUPS]
        if value not in valid_groups:
            raise serializers.ValidationError(f"Invalid blood group. Must be one of {valid_groups}")
        return value
    
    def validate_age(self, value):
        if value < 18 or value > 65:
            raise serializers.ValidationError("Age must be between 18 and 65")
        return value
