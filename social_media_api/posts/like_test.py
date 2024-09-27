from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Like
from rest_framework.authtoken.models import Token

User = get_user_model()

class LikeUnlikeTests(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='testpass123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='testpass123', email='user2@example.com')

        # Create a post for user1
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user1)

        # Create a token for user1
        self.token = Token.objects.create(user=self.user1)

        # Set the authorization header for user1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_like_post(self):
        url = reverse('like-post', args=[self.post.id])
        response = self.client.post(url)

        # Check that the like was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().user, self.user1)

    def test_like_post_already_liked(self):
        # Like the post first time
        url = reverse('like-post', args=[self.post.id])
        self.client.post(url)  # First like

        # Try to like the same post again
        response = self.client.post(url)

        # Check that the response is a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "You have already liked this post."})

    def test_unlike_post(self):
        # First, like the post
        self.client.post(reverse('like-post', args=[self.post.id]))

        # Now, unlike the post
        url = reverse('unlike-post', args=[self.post.id])
        response = self.client.delete(url)

        # Check that the like was removed successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_unlike_post_not_liked(self):
        # Try to unlike a post that was never liked
        url = reverse('unlike-post', args=[self.post.id])
        response = self.client.delete(url)

        # Check that the response is a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "You have not liked this post."})

    def test_like_post_not_authenticated(self):
        # Logout user
        self.client.logout()

        # Try to like a post without authentication
        url = reverse('like-post', args=[self.post.id])
        response = self.client.post(url)

        # Check that the response is a 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
