from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet


post_router = DefaultRouter()
post_router.register(r"", viewset=PostViewSet, basename="post")

app_name = "posts"
urlpatterns = []
urlpatterns += post_router.urls
