from .models import Post
from rest_framework import serializers

likes_count = serializers.SerializerMethodField()
is_liked = serializers.SerializerMethodField()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
    source="author.username",
    read_only=True
)
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "content",
            "created_at",
            "updated_at",
            "likes",
            "is_liked",
        ]
        read_only_fields = ["author"]
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        
        return False