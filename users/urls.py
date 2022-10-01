from django.urls import path


from users.views import KakaoSignInView

urlpatterns = [
    path("signin/kakao", KakaoSignInView.as_view()),
]
