from django.shortcuts import redirect

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.secrets_viewer import SecretsViewer


class KakaoSignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, requst, *args, **kwargs):

        secrets_viewer = SecretsViewer()
        oauths = secrets_viewer.get_secret("OAUTH")
        client_id = oauths["KAKAO"]["REST_API_KEY"]
        redirect_uri = "http://127.0.0.1:8000/api/v1/auth/signup/kakao/callback"

        kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"

        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

        return redirect(uri)


class KakaoSignUpCallBackAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        import requests

        # request access token to Kakao login api
        secrets_viewer = SecretsViewer()
        url = "https://kauth.kakao.com/oauth/token"
        code = request.query_params.get("code")

        if not code:
            error_msg = "인가 코드가 필요합니다."
            return Response(error_msg, status.HTTP_400_BAD_REQUEST)

        data = {
            "grant_type": "authorization_code",
            "client_id": secrets_viewer.get_secret("OAUTH")["KAKAO"]["REST_API_KEY"],
            "redirect_uri": "http://127.0.0.1:8000/api/v1/auth/signup/kakao/callback",
            "code": code,
        }

        token_response = requests.post(url, data)
        if token_response.status_code > 200:
            error_msg = "액세스 토큰을 받지 못했습니다."
            return Response(error_msg, status.HTTP_400_BAD_REQUEST)

        token_json = token_response.json()
        access_token = token_json.get("access_token")

        # request userdata to Kakao user api
        userdata_response = requests.get(
            url="https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        return Response(userdata_response.json())
