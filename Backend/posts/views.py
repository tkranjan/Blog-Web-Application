from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


from users.permissions import isUser

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class CreatePostView(APIView):
    permission_classes = [
        IsAuthenticated,
        isUser
    ]

    def post(self,request):
        data = request.data.copy()

        data['author'] = request.user.id

        serializer = PostSerializer(
            data = data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(author=request.user)

        return Response(serializer.data)

class PostListView(APIView):
    permission_classes = [
        AllowAny
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        "title",
        "content",
    ]

    filterset_fields = [
        "author",
    ]

    ordering_fields = [
        "created_at",
        "title",
    ]

    ordering = [
        "created_at",
    ]

    def get(self,request):
        queryset = Post.objects.all()

        for backend in self.filter_backends:
            queryset = backend().filter_queryset(
                request,
                queryset,
                self
            )

        serializer = PostSerializer(
            queryset,
            many = True
        )


        return Response(serializer.data)
    
class SinglePostView(APIView):
    permission_classes = [
        AllowAny
    ]

    def get(self,request,pk):

        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)

        return Response(serializer.data)
    
class PostUpdateView(APIView):
    permission_classes =[
        IsAuthenticated,
        isUser
    ]

    def put(self,request,pk):

        post = Post.objects.get(id=pk)

        if post.author != request.user:
            return Response({
                "error":"Not Allowed"
            },
            status=403
        )

        serializer = PostSerializer(
            post,
            data = request.data,
            partial = True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(serializer.data)
    

class PostDeleteView(APIView):
    permission_classes = [
        IsAuthenticated,
        isUser
    ]

    def delete(self,request,pk):
        post = get_object_or_404(Post,id=pk)

        if post.author != request.user:
            return Response({
                "error":"Not Allowed"
            },
            status=403
            )
        
        post.delete()

        return Response({
            "message":"Post Deleted"
        })
class ToggleLikeView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self,request,post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():

            post.likes.remove(request.user)

            return Response(
                {
                    "message":"Post Unliked",
                    "likes_count":post.likes.count()
                }
            )
        
        post.likes.add(request.user)

        return Response(
            {
                "message":"Post Liked",
                "likes_count":post.likes.count()
            }
        )
    
class BookmarkPostView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self,request,post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.bookmarks.filter(id=request.user.id).exists():

            post.bookmarks.remove(request.user)

            return Response(
                {
                    "message":"Post Removed from Bookmarks",
                    "bookmarks_count":post.bookmarks.count()
                }
            )
        
        post.bookmarks.add(request.user)

        return Response(
            {
                "message":"Post Bookmarked",
                "bookmarks_count":post.bookmarks.count()
            }
        )