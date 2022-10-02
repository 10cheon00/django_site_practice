from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import KakaoSignInView
from users.views import KakaoSignUpView

urlpatterns = [
    path("signin/kakao", KakaoSignInView.as_view()),
    path("signup/kakao", KakaoSignUpView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
]
