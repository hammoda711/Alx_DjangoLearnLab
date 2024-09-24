from .serializers import RegisterSerializer, TokenSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
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