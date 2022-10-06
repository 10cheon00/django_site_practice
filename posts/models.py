from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models


class Category(models.Model):
    name = models.CharField(default="category", max_length=100)


class Tag(models.Model):
    name = models.CharField(default="tag", max_length=100)


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(default="title", max_length=100)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    views = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    is_secret = models.BooleanField(default=False)
    is_notice = models.BooleanField(default=False)


def get_image_path(instance, filename):
    today = timezone.now()
    return f"images/{today.year}-{today.month}-{today.day}/{filename}"


class Image(models.Model):
    file = models.ImageField(upload_to=get_image_path)
    uploaded_date = models.DateTimeField(auto_now_add=True)
