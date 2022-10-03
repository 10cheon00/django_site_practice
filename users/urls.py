from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import KakaoLogInView
from users.views import KakaoRegistrationView
from users.views import PasswordLogInAPIView
from users.views import VerifyEmailAPIView
from users.views import EmailRegistrationAPIView

urlpatterns = [
    path("login/kakao", KakaoLogInView.as_view()),
    path("registration/kakao", KakaoRegistrationView.as_view()),
    path("login", PasswordLogInAPIView.as_view()),
    path("registration/email", EmailRegistrationAPIView.as_view()),
    path(
        "registration/email/verify", VerifyEmailAPIView.as_view(), name="verify-email"
    ),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
]
