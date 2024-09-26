from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from posts.models import Comment, Post

User = get_user_model()

class PostEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create test data
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.comment = Comment.objects.create(content='Test Comment', post=self.post, author=self.user)

    def test_create_post(self):
        data = {
            'title': 'Another Test Post',
            'content': 'Some more content.'
        }
        response = self.client.post('/api/posts/', data=data)
        self.assertEqual(response.status_code, 201)  # Check status code
        self.assertEqual(response.data['title'], 'Another Test Post')
        self.assertEqual(response.data['author_mail'], self.user.email)  # Verify author email
        self.assertEqual(response.data['author_name'], self.user.username)  # Verify author username

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)  # Check status code
        self.assertEqual(len(response.data), 1)  # Should only contain the post created in setUp

    def test_retrieve_post(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)  # Check status code
        self.assertEqual(response.data['title'], self.post.title)

    def test_update_post(self):
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated content.'
        }
        response = self.client.put(f'/api/posts/{self.post.id}/', data=data)
        self.assertEqual(response.status_code, 200)  # Check status code
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204)  # Check status code
        self.assertEqual(Post.objects.count(), 0)

    def test_create_comment(self):
        data = {
            'content': 'Another Test Comment'
        }
        response = self.client.post(f'/api/posts/{self.post.id}/comments/', data=data)
        self.assertEqual(response.status_code, 201)  # Check status code
        self.assertEqual(response.data['content'], 'Another Test Comment')
        self.assertEqual(response.data['author_mail'], self.user.email)

    def test_list_comments(self):
        response = self.client.get(f'/api/posts/{self.post.id}/comments/')
        self.assertEqual(response.status_code, 200)  # Check status code
        self.assertEqual(len(response.data), 1)  # Should only contain the comment created in setUp

    def test_update_comment(self):
        comment = Comment.objects.first()
        data = {
            'content': 'Updated Comment'
        }
        response = self.client.put(f'/api/posts/{self.post.id}/comments/{comment.id}/', data=data)
        self.assertEqual(response.status_code, 200)  # Check status code
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated Comment')

    def test_delete_comment(self):
        comment = Comment.objects.first()
        response = self.client.delete(f'/api/posts/{self.post.id}/comments/{comment.id}/')
        self.assertEqual(response.status_code, 204)  # Check status code
        self.assertEqual(Comment.objects.count(), 0)
