from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve
from .models import Posts


UserModel = get_user_model()


# モデルのテスト
class PostManagerTest(TestCase):
    def test_public_post_manager(self):
        user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )
        Posts.objects.create(content='content1', user=user)
        Posts.objects.create(content='content2', user=user)
        posts = Posts.objects.all()
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].content, 'content1')
        self.assertEqual(posts[0].user.username, 'test')