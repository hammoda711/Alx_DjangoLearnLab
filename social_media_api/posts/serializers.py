from .models import Comment,Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author_mail = serializers.ReadOnlyField(source='author.email')
    author_name = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'author_mail', 'author_name','title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
        

class CommentSerializer(serializers.ModelSerializer):
    author_mail = serializers.ReadOnlyField(source='author.email')
    author_name = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = ['id','author_mail', 'author_name','content','created_at','updated_at']
        
        def create(self, validated_data):
            validated_data['author'] = self.context['request'].user
            return super().create(validated_data)