from django.contrib.auth import get_user_model

from rest_framework import serializers

from posts.models import Category
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name"
    )
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="nickname"
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "category",
            "title",
            "author",
            "content",
            "created_date",
            "modified_date",
            "tags",
            "views",
            "up_votes",
            "down_votes",
            "is_secret",
            "is_notice",
        )
