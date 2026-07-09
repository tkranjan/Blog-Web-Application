from django.db import models
from users.models import User
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True
    )

    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = "bookmarked_posts",
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_liked = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.title