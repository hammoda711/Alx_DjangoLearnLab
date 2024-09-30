# **Social Media API**

## Introduction

The **Social Media API** is a Django-based backend project that provides a RESTful API for a social media platform. Users can register, authenticate, create posts, comment on posts, follow other users, view a personalized feed of posts from users they follow and also get notification comments and likes on your posts, new followers, and new posts from users who use are following.

---

## Features

- User registration and authentication
- Create, retrieve, update, and delete posts
- Comment on posts
- Follow and unfollow other users
- Personalized feed of followed users posts
- Notifications for comments, likes, new followers, and new following posts

## Technology Stack

- **Framework:** Django
- **Database:** PostgreSQL
- **RESTful API:** Django REST framework

---

## Project Setup

### Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)
- Git

### Installation

1. **Clone the Repository**
  
  ```bash
  git clone https://github.com/hammoda711/SocialMediaAPI.git
  cd SocialMediaAPI/social_media_api
  ```
  
2. **Create a Virtual Environment**
  
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
  
3. **Install Dependencies**
  
  ```bash
  pip install -r requirements.txt
  ```
  
4. **Apply Migrations**
  
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
  

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

---

## API Endpoints

### Authentication-User Endpoints

- **Register:** `/api/accounts/register/`
  
  `POST` to register a new user.
  
- **Login:** `/api/accounts/login/`
  
  `POST` to authenticate a user.
  
- **User Profile:** `/api/accounts/profile/`
  
  `GET`, `PUT`, `PATCH` to retrieve or update the authenticated user's profile.
  
- **Follow User:** `/api/accounts/follow/<int:user_id>/`
  
  `POST` to follow a user by their ID.
  
- **Unfollow User:** `/api/accounts/unfollow/<int:user_id>/`
  
  `POST` to unfollow a user by their ID.
  

---

### Posts Endpoints

- **List/Create Posts:** `/api/posts/`
  
  `GET`, `POST` to list all posts or create a new post.
  
- **Retrieve/Update/Delete Post:** `/api/posts/<int:post_id>/`
  
  `GET`, `PUT`, `PATCH`, `DELETE` to retrieve, update, or delete a specific post.
  
- **Feed:** `/api/posts/feed/`
  
  `GET` to retrieve the user's feed.
  
- **Like Post:** `/api/posts/like/<int:post_id>/`
  
  `POST` to like a post by its ID.
  
- **Unlike Post:** `/api/posts/unlike/<int:post_id>/`
  
  `POST` to unlike a post by its ID.
  

---

### Comments Endpoints

- **List/Create Comments:** `/api/posts/<int:post_id>/comments/`
  
  `GET`, `POST` to list all comments for a post or add a new comment.
  
- **Retrieve/Update/Delete Comment:** `/api/posts/<int:post_id>/comments/<int:comment_id>/`
  
  `GET`, `PUT`, `PATCH`, `DELETE` to retrieve, update, or delete a specific comment.
  

---

### Notifications Endpoints

- **List Notifications:** `/api/notifications/`
  
  `GET` to retrieve a list of notifications for the user.
  

---

## Testing

Testing is crucial to ensure all endpoints work as expected.

### Manual Testing with Postman

Use Postman to send requests to each endpoint:

- User Registration and Authentication
  
- Post and Comment Operations
  
- Follow and Feed
  

### Automated Testing

Consider writing automated tests using Django's testing framework, we create unit test cases for:

- user authentation in `accounts/tests.py` and `accounts/follow_test.py`
  
- posts and other related functionalities in `posts/tests.py` and `posts/like_test.py`
  

**Example (`tests.py`):**

```python
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
```

---

## Additional Notes

- **Pagination:** Implemented using Django REST Framework's built-in pagination classes.
- **Filtering:** Posts can be filtered by title or content using query parameters.
- **Permissions:** Only authenticated users can create, update, or delete content. Users can only modify their own posts and comments.
- **Authentication:** Token-based authentication is used for securing the API endpoints.
- **Best Practices:**
  - Ensure to limit the permissions of the database user (`social_user`) to only the necessary privileges.
  - Use environment variables to manage sensitive information like database credentials.
- **Media Files:** Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py` for handling profile pictures.

**Example Configuration in `settings.py`:**

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**URL Configuration in `urls.py`:**

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your url patterns ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## How to Use the API

**Example (`User APIs`):**

1. **Register a New User**
  
  Send a `POST` request to `/api/accounts/register/` with user details.
  
2. **Authenticate**
  
  Send a `POST` request to `/api/accounts/login/` to receive an authentication token.
  
3. **Include the Token**
  
  For authenticated requests, include the token in the `Authorization` header:
  
  ```
  Authorization: Bearer your-auth-token
  ```
  
4. **Interact with the API**
  
  Use the provided endpoints to create posts, comment, follow users, and view your feed.
  

---

## Conclusion

This Social Media API provides a solid foundation for a social media platform, including user authentication, post and comment management, like and notification, user following capabilities, and a personalized feed. Further enhancements can include features like direct messaging and more robust security measures.

---

## Repository Structure

```
SocialMediaAPI/
├── social_media_api/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
|   |   ├── follow_test.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── posts/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
|   |   ├── like_test.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── social_media_api/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
└── README.md
```

---

## Contact Information

For any questions or contributions, please contact:

- **Author:** ***Mohamed Taher***
- **Email:** [Gmail]([mo.taher717@gmail.com])
- **GitHub:** [Mohamed Taher]([https://github.com/hammoda711])
