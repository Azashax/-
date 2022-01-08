from django.urls import path

from .views import (
    RegistrationApiView,
    LoginAPIView,
    AllUsers, RefreshView, LogoutView, UserRetrieveUpdateAPIView, UserProfileUpdateAPIView)
from .base_auth.telegram_auth import TelegramAuthAPIView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('login/telegram/', TelegramAuthAPIView.as_view()),
    path('login/telegram/update', UserProfileUpdateAPIView.as_view()),
    path('all_users/', AllUsers.as_view()),
    path('profile/', UserRetrieveUpdateAPIView.as_view()),
    path('register/', RegistrationApiView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('logout/', LogoutView.as_view())
]
