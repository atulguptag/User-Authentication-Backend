from django.urls import path
from user_api import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.LoginView.as_view(), name='auth_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cinemas/', views.CinemaListCreateAPIView.as_view(), name='cinema-list'),
    path('cinemas/<int:pk>/', views.CinemaRetrieveUpdateDestroyAPIView.as_view(), name='cinema-detail'),
    path('cinema_halls/', views.CinemaHallListCreateAPIView.as_view(), name='cinema-hall-list'),
    path('cinema_halls/<int:pk>/', views.CinemaHallRetrieveUpdateDestroyAPIView.as_view(), name='cinema-hall-detail'),
    path('cinema_seats/', views.CinemaSeatListCreateAPIView.as_view(), name='cinema-seat-list'),
    path('cinema_seats/<str:pk>/', views.CinemaSeatRetrieveUpdateDestroyAPIView.as_view(), name='cinema-seat-detail'),
    path('movies/', views.MovieListCreateAPIView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-detail'),
    path('shows/', views.ShowListCreateAPIView.as_view(), name='show-list'),
    path('shows/<int:pk>/', views.ShowRetrieveUpdateDestroyAPIView.as_view(), name='show-detail'),
    path('tickets/', views.TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
    path('logs/', views.LogListCreateAPIView.as_view(), name='log-list'),
    path('logs/<int:pk>/', views.LogRetrieveUpdateDestroyAPIView.as_view(), name='log-detail'),
]
