from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class EmailRegistrationTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.registration_url = reverse("email-registration")
        self.form_data = {
            "username": "user01",
            "password": "password01",
            "nickname": "nickname01",
            "email": "10cheon00@naver.com",
            "favorate_race": "zerg",
        }

    def test_success_registration(self):
        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_registration_with_wrong_email(self):
        """Registering with wrong email format will be fail."""

        form_data = self.form_data
        form_data["email"] = "wrong_email@wrong_email.com"
        response = self.client.post(path=self.registration_url, data=form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_registration_with_wrong_favorate_race(self):
        """Registering with value what not allowed in choices will be fail."""

        form_data = self.form_data
        form_data["favorate_race"] = "wrong_race"
        response = self.client.post(path=self.registration_url, data=form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_registration_with_already_exist_user(self):
        """Registering with already exist data will be fail."""

        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_sending_verification_email_while_registration(self):
        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Verify your email")

    def test_success_email_verification(self):
        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verification_url = mail.outbox[0].body.split("\n", 1)[1]
        response = self.client.get(path=verification_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_email_verification_with_wrong_token(self):
        """Verifying with wrong token will be fail"""

        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verification_url = mail.outbox[0].body.split("\n", 1)[1]
        verification_url = verification_url[:-3] + "ABC"

        response = self.client.get(path=verification_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_email_verification_with_expired_token(self):
        """Verifying with expired token will be failed"""

        response = self.client.post(path=self.registration_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0Nzc3NDM3LCJpYXQiOjE2NjQ3NzcxMzcsImp0aSI6IjA5YjJiNWUwY2FiMjQ3ZjRiOTg5MTQyOWIzOTczNjI1IiwidXNlcl9pZCI6MX0.N_i60m0deO9FHA0VQ662AVKywSF2KaXVjlOti7E35sE"
        verification_url = mail.outbox[0].body.split("\n", 1)[1]
        verification_url = (
            verification_url.split("token", 1)[0] + "token=" + expired_token
        )

        response = self.client.get(path=verification_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
