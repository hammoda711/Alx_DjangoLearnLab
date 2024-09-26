from rest_framework import serializers
from django .contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

#to dynamically get the user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','email','bio','followers','profile_picture',]

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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password', 'bio', 'profile_picture', 'followers']
        read_only_fields = ['email', 'followers']
        
        #validate the updated data
        '''def update(self, instance, validated_data):
            # Update profile fields
            instance.bio = validated_data.get('bio', instance.bio)
            instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
            instance.save()
            return instance
            '''
        
class FollowUserSerializer(serializers.Serializer):
    followed_user_id = serializers.IntegerField()
    # validates whether the user with the given ID exists.
    def validate_followed_user_id(self, value):
        try:
            followed_user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value