from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from django.template.loader import render_to_string
from .serializers import RegisterSerializer, UserLoginSerializer
from rest_framework.authentication import TokenAuthentication
from .validations import validate_username, validate_password
from . import models as m

# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response({"success": "Successfully Logged In"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)


# Forgot Password View -
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate a secure password reset token using django-allauth (recommended)
        token_generator = PasswordResetTokenGenerator()
        reset_token = token_generator.make_token(user)

        # Create or update the PasswordResetRequest model instance
        password_reset_request = m.PasswordResetRequest.objects.get_or_create(
            user=user, email=user.email
        )
        password_reset_request.reset_token = reset_token
        password_reset_request.save()

        current_site = get_current_site(request)
        mail_subject = 'Reset Your Account Password'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_token': reset_token,
            'current_site': current_site,
            'domain': current_site.domain,  # Use current_site.domain
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        })
        email = EmailMessage(mail_subject, message,
                             settings.EMAIL_HOST_USER, [user.email])
        email.send()

        return Response({'message': 'Password reset link sent to your email address.'})


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        new_password = request.data.get('new_password1')

        if uidb64 is None or token is None:
            return Response({'error': 'Invalid request.'}, status=400)

        try:
            user_id = int(urlsafe_base64_decode(
                uidb64).decode('utf-8'))  # Use int() directly
            user = User.objects.get(pk=user_id)
        except (ValueError, User.DoesNotExist):
            return Response({'error': 'Invalid link.'}, status=400)

        # Check if the token is valid (using django-allauth)
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=400)

        # Set the new password
        user.set_password(new_password)
        user.save()
        login(request, user)  # Import login from django.contrib.auth

        return Response({'message': _('Password reset successfully.')})
