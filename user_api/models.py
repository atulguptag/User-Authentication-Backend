from django.db import models
from django.contrib.auth.models import User
from datetime import timezone

class Cinema(models.Model):
    cinema_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    district = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'cinema'

class CinemaHall(models.Model):
    HALL_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    cinema_hall_id = models.AutoField(primary_key=True)
    hall_size = models.CharField(max_length=1, choices=HALL_SIZES)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cinema_hall'

class CinemaSeat(models.Model):
    cinema_seat_id = models.CharField(primary_key=True, max_length=45)
    booked_shows = models.CharField(max_length=1000, default="")
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    row_no = models.CharField(max_length=45)
    col_no = models.CharField(max_length=45)

    class Meta:
        db_table = 'cinema_seat'

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    poster = models.CharField(max_length=45)
    title = models.CharField(max_length=100, default="Untitled")
    year = models.PositiveIntegerField(default="2022")
    genre = models.CharField(max_length=100)
    date = models.DateTimeField()
    end_date = models.DateTimeField()
    actors = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    director = models.CharField(max_length=45)
    duration = models.CharField(max_length=45)
    language = models.CharField(max_length=45)
    about = models.CharField(max_length=1024)
    score = models.FloatField(null=True, blank=True, default=None)
    in_theatre = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'movie'

class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'show'

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add=True)
    seats = models.CharField(max_length=1000, default="")

    class Meta:
        db_table = 'ticket'

class Log(models.Model):
    message = models.CharField(max_length=255)
    level = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

# Forgot Password
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    reset_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # Set an expiry time for the reset token (e.g., 24 hours)
    expiry = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Password reset request for {self.user.email}"

    def is_valid(self):
        # Check if the token is not expired
        return self.expiry is None or self.expiry > timezone.now()
    

# from django.db import models
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractUser, PermissionsMixin

# # Create your models here.
# class AppUserManager(BaseUserManager):
# 	def create_user(self, email, username, password=None):
# 		if not email:
# 			raise ValueError('An email is required.')
# 		##
# 		if not username:
# 			raise ValueError("An username is required.")
# 		##
# 		if not password:
# 			raise ValueError('A password is required.')

# 		email = self.normalize_email(email)
# 		user = self.model(email=email)
# 		user.set_password(password)
# 		user.save()
# 		return user

# 	def create_superuser(self, email, username, password=None):
# 		if not email:
# 			raise ValueError('An email is required.')
# 		##
# 		if not username:
# 			raise ValueError("An username is required.")
# 		##
# 		if not password:
# 			raise ValueError('A password is required.')

# 		user = self.create_user(email, username, password)
# 		user.is_superuser = True
# 		user.save()
# 		return user

# class AppUser(AbstractUser, PermissionsMixin):
# 	user_id = models.AutoField(primary_key=True)
# 	email = models.EmailField(max_length=50, unique=True)
# 	username = models.CharField(max_length=50)
# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['username']
# 	objects = AppUserManager()
# 	def __str__(self):
# 		return self.email
