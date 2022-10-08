from sqlite3 import paramstyle
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Category
from posts.models import Post


class PostModelViewSet(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="General")
        self.list_url = reverse("posts:post-list")
        self.user = get_user_model().objects.create(username="user", nickname="User")

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()

    def test_create_post(self):
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": "Hello!",
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_all_post(self):
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": "Hello!",
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(path=self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_post(self):
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": "Hello!",
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("posts:post-detail", kwargs={"pk": response.data["id"]})
        response = self.client.get(path=detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], self.user.nickname)

    def test_update_post(self):
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": "Hello!",
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = response.data
        post["content"] = "<p>Hello, World!</p>"
        detail_url = reverse("posts:post-detail", kwargs={"pk": post["id"]})

        response = self.client.put(path=detail_url, data=post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(path=detail_url)
        self.assertEqual(response.data["content"], post["content"])

    def test_delete_post(self):
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": "Hello!",
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("posts:post-detail", kwargs={"pk": response.data["id"]})
        response = self.client.delete(path=detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(path=detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_included_XSS_attack_scripts(self):
        content = "<p>Hello!</p>"
        xss_content = content + "<script>alert('warning');</script>"
        post_data = {
            "title": "Title",
            "category": self.category,
            "author": self.user,
            "content": xss_content,
        }
        response = self.client.post(path=self.list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("posts:post-detail", kwargs={"pk": response.data["id"]})
        response = self.client.get(path=detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], content)
