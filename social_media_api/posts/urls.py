from django.urls import include, path
from .views import CommentViewSet, FeedView, LikePostView, PostViewSet, UnlikePostView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike-post'),

]