from django.urls import include, path
from .views import PostViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),

]