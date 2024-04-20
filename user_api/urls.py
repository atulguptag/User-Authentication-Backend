from django.urls import path
from user_api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.LoginView.as_view(), name='auth_login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
]
