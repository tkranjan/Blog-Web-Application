from django.urls import path
from .views import (
    CreateCommentView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path("create/",CreateCommentView.as_view(),name="create-comment"),
    path("<int:pk>/",CommentUpdateView.as_view(),name="update-comment"),
    path("<int:pk>/delete/",CommentDeleteView.as_view(),name="delete-comment"),
]