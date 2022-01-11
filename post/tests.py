from django.http import response
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


class CreatePostTest(TestCase):
    '''ログインしたユーザーが投稿を作成し、登録処理されることを検証'''

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )
        self.client.force_login(self.user) # ユーザーログイン
    
    def test_render_creation_form(self):
        response = self.client.get('/post/create_post')
        self.assertContains(response, '投稿する', status_code=200)
    
    def test_create_post(self):
        data = {
            'content': 'テスト',
        }
        self.client.post('/post/create_post', data)
        post = Posts.objects.get(content='テスト')
        self.assertEqual('テスト', post.content)
        self.assertEqual(self.user.username, post.user.username)


class PostDetailTest(TestCase):
    '''
    ユーザーがログイン後に投稿を作成し、
    投稿詳細ページに投稿内容が表示されることを検証
    '''

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )
        self.client.force_login(self.user) # ユーザーログイン
        self.post = Posts.objects.create(
            content='テスト',
            user=self.user,
        )
    
    def test_should_use_expected_template(self):
        response = self.client.get('/post/post_detail/%s' % self.post.id)
        self.assertTemplateUsed(response, 'post/post_detail.html')
    
    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get('/post/post_detail/%s' % self.post.id)
        self.assertContains(response, self.post.content, status_code=200)
