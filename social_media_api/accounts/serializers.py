from rest_framework import serializers
from django .contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

#to dynamically get the user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email','bio','followers','profile_picture',]

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        attrs['user'] = user 
        return attrs #attrs={user:pass}
    