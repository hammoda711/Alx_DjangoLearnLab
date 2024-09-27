from .models import Comment, Like,Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author_mail = serializers.ReadOnlyField(source='author.email')
    author_name = serializers.ReadOnlyField(source='author.username')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'author_mail', 'author_name','title', 'content', 'created_at', 'updated_at','comments']
        
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

        extra_kwargs = {'post_id': {'required': True}}#in the CommentViewSet  
        
        def create(self, validated_data):
            request = self.context.get('request')
            validated_data['author'] = request.user
            return super().create(validated_data)



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']
        read_only_fields = ['user']