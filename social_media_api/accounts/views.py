from django.shortcuts import get_object_or_404

from notifications.utils import create_notification
from .serializers import ProfileSerializer, RegisterSerializer, TokenSerializer, LoginSerializer,FollowUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# Create your views here.
#to dynamically get the user model
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    #queryset = User.objects.all()
    serializer_class = RegisterSerializer


    def perform_create(self, serializer):
        #serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user
        
        # Create a token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'token': token.key,
        }, status=201)
    

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Necessary for login
        user = serializer.validated_data['user']  # Get the authenticated user
        # Token retrieval
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'token': token.key,
        }, status=201)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




# Follow user view
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer

    def post(self, request, *args, **kwargs):
        followed_user_id = kwargs.get('user_id')
        followed_user = get_object_or_404(User, id=followed_user_id)

        # Check if the user is trying to follow themselves
        if followed_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already following the target user
        if followed_user in request.user.following.all():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the followed user to the current user's following list
        request.user.following.add(followed_user)

        # Generate a notification for the followed user
        create_notification(recipient=followed_user, actor=request.user, verb='followed you', target=None)

        return Response({"message": "You are now following this user."}, status=status.HTTP_201_CREATED)
    



class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer

    def delete(self, request, *args, **kwargs):
        unfollowed_user_id = kwargs.get('user_id')
        unfollowed_user = get_object_or_404(User, id=unfollowed_user_id)

        # Check if the user is not following the target user
        if unfollowed_user not in request.user.following.all():
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        # Remove the followed user from the current user's following list
        request.user.following.remove(unfollowed_user)
        return Response(status=status.HTTP_204_NO_CONTENT)



