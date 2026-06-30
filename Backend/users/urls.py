from django.urls import path
from .views import (RegisterView,LoginView,
    RefreshView,LogoutView,
    ProfileView,
    ProfileUpdateView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('refresh/',RefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('profile/update/',ProfileUpdateView.as_view()),
    path('forgot-password/',ForgotPasswordView.as_view(),name="forgot-password"),
    path('reset-password/<uidb64>/<token>/',ResetPasswordView.as_view(),name="reset-password"),
]