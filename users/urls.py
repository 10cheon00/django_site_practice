from django.urls import path


from users.views import KakaoSignInView
from users.views import KakaoSignUpView

urlpatterns = [
    path("signin/kakao", KakaoSignInView.as_view()),
    path("signup/kakao", KakaoSignUpView.as_view()),
]
