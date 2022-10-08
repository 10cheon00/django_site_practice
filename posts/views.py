from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
