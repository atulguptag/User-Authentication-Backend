from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User, PasswordResetRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

UserModel = get_user_model()

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValidationError('User not found with the given credentials!')
        return user

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username')


# Password Reset Request Serializer
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = ('email')


# Password Reset Serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data['email']
        new_password1 = data['new_password1']
        new_password2 = data['new_password2']

        if new_password1 != new_password2:
            raise serializers.ValidationError('Passwords must match.')

        # Check if email exists in the user database
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Email address not found.')

        return data

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()

        # Generate a secure password reset token
        reset_token = generate_password_reset_token(user)

        # Create or update the PasswordResetRequest model instance
        password_reset_request, created = PasswordResetRequest.objects.get_or_create(
            user=user, email=email
        )
        password_reset_request.reset_token = reset_token
        password_reset_request.save()

        # Send email with reset link (implementation details omitted)
        send_password_reset_email(user.email, reset_token)

        return user


def generate_password_reset_token(user):
    token_generator = PasswordResetTokenGenerator()
    return token_generator.make_token(user)


def send_password_reset_email(email, reset_token, request=None, user=None):
    # Get current site information
    current_site = request.get_host() if request else settings.ALLOWED_HOSTS[0]

    # Context data for the email template
    context = {
        'email': email,
        'reset_token': reset_token,
        'domain': current_site,
        'user': user,
    }

    # Render email template
    subject = 'Password Reset Instructions'
    message = render_to_string(
        'registration/password_reset_email.html', context)

    # Create and send email
    email_message = EmailMultiAlternatives(
        subject, message, settings.EMAIL_HOST_USER, [email])
    email_message.content_type = 'text/html; charset=UTF-8'
    email_message.send()
