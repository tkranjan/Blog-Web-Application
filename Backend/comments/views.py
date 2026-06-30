from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer

# Create your views here.
class CreateCommentView(APIView):
    permission_classes = [AllowAny]

    
    def post(self,request):

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ListCommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,post_id):
        comments = Comment.objects.filter(post_id=post_id)

        serializer = CommentSerializer(
            comments,
            many = True
        )

        return Response(serializer.data)
    
class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,pk):
        comment = get_object_or_404(Comment,pk=pk)

        if comment.user != request.user:
            return Response(
                {
                    "error":"You can't update other's comment"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CommentSerializer(
            comment,
            data = request.data
        )

        if serializer.is_valid():
            
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )
    

class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk):
        comment = get_object_or_404(Comment, pk = pk)

        if comment.user != request.user:
            return Response(
                {
                    "error":"You're not allowed to delete other's comment"
                },
                status = status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()

        return Response(
            {
                "message" : "Comment Deleted Successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )