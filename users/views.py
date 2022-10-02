import requests

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class KakaoException(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


def fetch_kakao_user_data(access_token):
    try:
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise KakaoException("잘못된 엑세스 토큰입니다.")

        user_data = response.json()
        return user_data
    except Exception as exception:
        raise exception


class KakaoSignInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        User = get_user_model()
        try:
            access_token = request.data["access_token"]
            kakao_user_data = fetch_kakao_user_data(access_token)
            kakao_user_id = kakao_user_data["id"]

            user = User.objects.filter(
                kakao_id=kakao_user_id, registration_type="kakao"
            )
            if not user.exists():
                raise User.DoesNotExist("가입되지 않은 사용자입니다.")

            refresh = RefreshToken.for_user(user.first())
            data = {"access": str(refresh.access_token), "refresh": str(refresh)}
            return Response(data=data, status=status.HTTP_200_OK)

        except KeyError as key:
            error_msg = f"{str(key)}필드에 오류가 있습니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class KakaoSignUpView(APIView):
    def post(self, request):
        User = get_user_model()
        try:
            access_token = request.data["access_token"]
            kakao_user_data = fetch_kakao_user_data(access_token)
            kakao_user_id = kakao_user_data["id"]

            user = User.objects.filter(
                kakao_id=kakao_user_id, registration_type="kakao"
            )
            if user.exists():
                raise UserAlreadyExists("이미 가입되어있는 유저입니다.")

            username = kakao_user_id
            nickname = request.data["nickname"]
            extra_fields = {
                "favorate_race": request.data["favorate_race"],
                "registration_type": "kakao",
                "kakao_id": username,
            }
            created_user = User.objects.create_user(
                username=username, nickname=nickname, **extra_fields
            )

            refresh = RefreshToken.for_user(created_user)
            data = {"access": str(refresh.access_token), "refresh": str(refresh)}
            return Response(data=data, status=status.HTTP_200_OK)
        except KeyError as e:
            error_msg = f"{str(e)}필드에 오류가 있습니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
