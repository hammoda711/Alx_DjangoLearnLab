from rest_framework import viewsets, permissions, serializers
from rest_framework.filters import SearchFilter
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post,Comment
from .serializers import CommentSerializer, PostSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination

# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True

            return obj.author == request.user 

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']
    pagination_class = PageNumberPagination
    
    def get_object(self):
        author = super().get_object()
        # No need for additional permission check here 
        # because of the custom permission (IsAuthorOrReadOnly)
        return author  
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PageNumberPagination
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk') 
    # Retrieve post_id from URL parameter
        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
                serializer.save(author=self.request.user, post=post)
            except Post.DoesNotExist:
                raise serializers.ValidationError("Invalid post ID provided.")
        else:
            raise serializers.ValidationError("Missing post ID in request.")

    def get_object(self):
        comment = super().get_object()
        return comment



    