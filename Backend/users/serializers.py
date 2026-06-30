from rest_framework import serializers
from .models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.conf import settings
from rest_framework import serializers

from utils.emails import (send_reset_password_email,
                          send_password_reset_confirmation_email,
                          user_registeration_confirmation_email,
                        )

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
            'password',
            'role',
            'email',
            'first_name',
            'last_name'
        ]
        
        extra_kwargs = {'password': {'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data) #Ensures password is hashed
    
        user_registeration_confirmation_email(
            to_email = user.email,
            username = user.username,
        )

        return user

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    password = serializers.CharField(write_only=True)

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'bio'
        ]

User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        if not User.objects.filter(email = value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist."
            )
        
        return value
    
    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = PasswordResetTokenGenerator().make_token(
            user
        )

        reset_link = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password/{uid}/{token}/"
        )

        send_reset_password_email(
            to_email=email,
            reset_link=reset_link,
            username=user.username,
        )

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True,min_length=8)

    def validate(self,attrs):
        if (attrs["new_password"]!= attrs["confirm_password"]):
            raise serializers.ValidationError(
                "Password do not match."
            )
        
        return attrs
    
    def save(self,uidb64,token):
        try:
            uid = force_str(
                urlsafe_base64_decode(uidb64)
            )
            user = User.objects.get(pk=uid)

        except Exception:
            raise serializers.ValidationError(
                "Invalid Reset Link."
            )
        
        if not PasswordResetTokenGenerator().check_token(
            user,
            token
        ):
            raise serializers.ValidationError(
                "Invalid Token or Token Expired"
            )
        
        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        send_password_reset_confirmation_email(
            to_email=user.email,
            username= user.username,
            )

        return user
    
            

