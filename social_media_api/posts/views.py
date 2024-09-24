
from rest_framework import viewsets, permissions,filters
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django_filters import rest_framework



# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True

            return obj.author == request.user 

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']
    
    