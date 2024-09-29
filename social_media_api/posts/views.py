from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, serializers, generics, status
from rest_framework.filters import SearchFilter

from notifications.utils import create_notification  # Import notification utility
from .models import Like, Post, Comment
from .serializers import CommentSerializer, LikeSerializer, PostSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Custom permission class
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# Post viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        
        # Notification for followers when user creates a new post
        followers = self.request.user.followers.all()
        for follower in followers:
            create_notification(recipient=follower, actor=self.request.user, verb='posted a new post', target=post)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
                comment = serializer.save(author=self.request.user, post=post)

                # Generate a notification for post author when someone comments
                create_notification(recipient=post.author, actor=self.request.user, verb='commented on your post', target=comment)

            except Post.DoesNotExist:
                raise serializers.ValidationError("Invalid post ID provided.")
        else:
            raise serializers.ValidationError("Missing post ID in request.")

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')

class LikePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        # Generate a notification for post author when someone likes the post
        create_notification(recipient=post.author, actor=request.user, verb='liked your post', target=post)

        if created:
            return Response({"message": "Liked post."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
