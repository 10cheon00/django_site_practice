from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailRegistrationAPIView
from users.views import KakaoLogInView
from users.views import KakaoRegistrationView
from users.views import VerifyEmailAPIView


urlpatterns = [
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("login/kakao", KakaoLogInView.as_view(), name="kakao-login"),
    path(
        "registration/kakao", KakaoRegistrationView.as_view(), name="kakao-registration"
    ),
    path(
        "registration/email",
        EmailRegistrationAPIView.as_view(),
        name="email-registration",
    ),
    path(
        "registration/email/verify",
        VerifyEmailAPIView.as_view(),
        name="email-verification",
    ),
]
