from .models import Post
from rest_framework import serializers

likes_count = serializers.SerializerMethodField()
is_liked = serializers.SerializerMethodField()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
             "id",
            "title",
            "content",
            "user",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def is_liked(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        
        return False