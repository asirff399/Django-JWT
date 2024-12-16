from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id','first_name','last_name','username','email']

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields= ['first_name','last_name','username','email','password','confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            password = validated_data.get('password'),
        )
        return user  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True,write_only=True)