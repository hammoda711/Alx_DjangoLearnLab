from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()
class ProfileEndpointTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        # Create an auth token for the test user
        self.token = Token.objects.create(user=self.user)

    def test_authenticated_profile_access(self):
        # Set the authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Make a GET request to the profile endpoint
        response = self.client.get(reverse('profile'))
        
        # Debug prints
        print("Token:", self.token.key)
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    
        # Test case for unauthenticated profile access
    def test_unauthenticated_profile_access(self):
        response = self.client.get(reverse('profile'))  # Replace 'profile' with your actual URL name
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expect 401


