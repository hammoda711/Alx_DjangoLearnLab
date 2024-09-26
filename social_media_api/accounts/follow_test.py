from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class FollowUnfollowTests(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')
        
        # Create tokens for the users
        self.token1, _ = Token.objects.get_or_create(user=self.user1)
        self.token2, _ = Token.objects.get_or_create(user=self.user2)

    def test_follow_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1.key))  # Use key to authorize
        url = reverse('follow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_non_existent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1.key))
        url = reverse('follow-user', kwargs={'user_id': 999})  # Assuming this user does not exist
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1.key))
        url = reverse('follow-user', kwargs={'user_id': self.user1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1.key))
        self.user1.following.add(self.user2)  # Make user1 follow user2
        url = reverse('unfollow-user', kwargs={'user_id': self.user2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Additional tests for other scenarios can be added here.
