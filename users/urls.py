from django.urls import path

from users.views import KakaoSignUpAPIView
from users.views import KakaoSignUpCallBackAPIView

urlpatterns = [
    path("signup/kakao", KakaoSignUpAPIView.as_view()),
    path("signup/kakao/callback", KakaoSignUpCallBackAPIView.as_view()),
]
