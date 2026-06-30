from .views import (
    CreatePostView,PostListView,
    SinglePostView,PostUpdateView,
    PostDeleteView,ToggleLikeView,
    BookmarkPostView,
)
from django.urls import path
from comments.views import ListCommentView

urlpatterns = [
    path('create/',CreatePostView.as_view()),
    path('',PostListView.as_view()),
    path('<int:pk>/',SinglePostView.as_view()),
    path('<int:pk>/update/',PostUpdateView.as_view()),
    path('<int:pk>/delete/',PostDeleteView.as_view()),
    path('<int:post_id>/comments/',ListCommentView.as_view(),name="list-comments"),
    path('<int:post_id>/toggle-like/',ToggleLikeView.as_view(),name="toggle-like"),
    path('<int:post_id>/toggle-bookmark/',BookmarkPostView.as_view(),name="toggle-bookmark"),
]