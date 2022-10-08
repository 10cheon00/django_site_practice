from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "category",
            "title",
            "author",
            "text",
            "created_date",
            "modified_date",
            "tags",
            "views",
            "up_votes",
            "down_votes",
            "is_secret",
            "is_notice",
        )
