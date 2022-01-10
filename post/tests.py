from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve
import random

from post.forms import CreatePostForm
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


# フォームのテスト
class PostFormTest(TestCase):
    def test_valid_when_given_more_than_140_content(self):
        chars = '23456789abcdefghijkmnopqrstuvwxzy'
        random_str = ''.join([random.choice(chars) for _ in range(141)])
        params = {
            'content': random_str,
        }
        post = Posts()
        form = CreatePostForm(params, instance=post)
        self.assertFalse(form.is_valid())
    
    def test_valid_when_given_with_140_content(self):
        chars = '23456789abcdefghijkmnopqrstuvwxzy'
        random_str = ''.join([random.choice(chars) for _ in range(140)])
        params = {
            'content': random_str,
        }
        post = Posts()
        form = CreatePostForm(params, instance=post)
        self.assertTrue(form.is_valid())