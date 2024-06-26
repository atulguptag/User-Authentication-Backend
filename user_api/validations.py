from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('Email already exists!')

    if not username or UserModel.objects.filter(username=username).exists():
        raise ValidationError('Username already exixts!')
    
    if not password or len(password) < 8:
        raise ValidationError('Password must be 8 characters')
    
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('An email is required!')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('An username is required!')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('A password is requuired!')
    return True