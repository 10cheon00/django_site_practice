from datetime import datetime
from unittest.mock import Mock
from unittest.mock import patch
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from django.db.utils import IntegrityError

from rest_framework.test import APITestCase

from posts.models import Category
from posts.models import Post


class CategoryModelTest(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Category.objects.all().delete()

    def test_name_max_length(self):
        max_length = Category._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_unique_constraint(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name="General")
            Category.objects.create(name="General")


class PostModelTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="username",
            password="password",
            nickname="nickname",
            favorate_race="zerg",
            email="email@email.com",
            is_verified=True,
        )
        self.category = Category.objects.create(name="general")

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()

    def test_title_max_length(self):
        max_length = Post._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_foreignkey_cascade(self):
        fields = Post._meta.get_fields()
        for field in fields:
            if isinstance(field, models.ForeignKey):
                self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_category_related_name(self):
        related_name = Post._meta.get_field("category").related_query_name()
        self.assertEqual(related_name, "posts")

    def test_author_related_name(self):
        related_name = Post._meta.get_field("author").related_query_name()
        self.assertEqual(related_name, "posts")

    def test_tag_related_name(self):
        related_name = Post._meta.get_field("tags").related_query_name()
        self.assertEqual(related_name, "posts")

    def test_default_values(self):
        mock_datetime = datetime(2000, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Seoul"))

        with patch("django.utils.timezone.now", Mock(return_value=mock_datetime)):
            post = Post.objects.create(
                title="title", author=self.user, category=self.category
            )
            self.assertEqual(post.created_date, mock_datetime)
            self.assertEqual(post.modified_date, mock_datetime)
            self.assertEqual(post.tags.count(), 0)
            self.assertEqual(post.views, 0)
            self.assertEqual(post.up_votes, 0)
            self.assertEqual(post.down_votes, 0)
            self.assertFalse(post.is_secret)
            self.assertFalse(post.is_notice)

    def test_success_update_modified_date(self):
        zoneinfo = ZoneInfo("Asia/Seoul")
        mock_created_datetime = datetime(2000, 1, 1, 0, 0, 0, tzinfo=zoneinfo)
        mock_datetime = Mock(return_value=mock_created_datetime)
        with patch("django.utils.timezone.now", new=mock_datetime):
            post = Post.objects.create(
                title="title",
                author=self.user,
                category=self.category,
            )

        mock_modified_datetime = datetime(2000, 1, 1, 0, 1, 0, tzinfo=zoneinfo)
        mock_datetime = Mock(return_value=mock_modified_datetime)

        with patch("django.utils.timezone.now", mock_datetime):
            post.title = "modified title"
            post.save()
            self.assertEqual(post.modified_date, mock_modified_datetime)
