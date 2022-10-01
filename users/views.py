import requests

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class KakaoException(Exception):
    pass


class KakaoSignInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            access_token = request.data["access_token"]

            url = "https://kapi.kakao.com/v2/user/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            kakao_user_data_response = requests.get(url=url, headers=headers)

            if kakao_user_data_response.status_code != 200:
                raise KakaoException()

            kakao_user_data = kakao_user_data_response.json()["kakao_account"]
            kakao_user_email = kakao_user_data["email"]

            user = get_user_model().objects.get(
                email=kakao_user_email, registration_type="kakao"
            )
            if user:
                refresh = RefreshToken.for_user(user)
                data = {"access": str(refresh.access_token), "refresh": str(refresh)}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist

        except KeyError:
            error_msg = "잘못된 요청입니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except KakaoException:
            error_msg = "잘못된 엑세스 토큰입니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            error_msg = "가입되지 않은 유저입니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
