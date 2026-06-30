from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields =[
            "id",
            "post",
            "user",
            "username",
            "content",
            "is_edited",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "username",
            "is_edited",
            "created_at",
            "updated_at",
        ]
