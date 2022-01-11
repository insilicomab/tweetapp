from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve
from .views import top, AboutView


UserModel = get_user_model()

'''
topページ
'''

class TopPageRenderTest(TestCase):
    '''ログインしていないユーザーがtopページにアクセスしたときのテスト'''

    def test_should_return_top_page_title(self):
        response = self.client.get('/')
        self.assertContains(response, 'つぶやきで、世界はつながる', status_code=200)
    
    def test_should_use_expected_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accounts/top.html')
    
    def test_should_resolve_top(self):
        found = resolve('/')
        self.assertEqual(top, found.func)


class LoginUserTopPageRedirectTest(TestCase):
    '''
    ログイン済みユーザーがTopページにGETリクエストすると
    投稿一覧ページにリダイレクトされることを検証
    '''

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )

    def test_loggedin_user_get_top_redirected_to_post_index(self):
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/')
        self.assertRedirects(response, '/post/posts_index')


'''
aboutページ
'''

class AboutPageRenderTest(TestCase):
    '''ログインしていないユーザーがaboutページにアクセスしたときのテスト'''

    def test_should_return_about_page_title(self):
        response = self.client.get('/about')
        self.assertContains(response, 'TweetAppとは', status_code=200)
    
    def test_should_use_expected_template(self):
        response = self.client.get('/about')
        self.assertTemplateUsed(response, 'accounts/about.html')

    def test_should_resolve_about(self):
        found = resolve('/about')
        self.assertEqual(AboutView, found.func.view_class)


'''
registページ
'''

class LoginUserRegistPageRedirectTest(TestCase):
    '''
    ログイン済みユーザーがサインアップページにGETリクエストすると
    投稿一覧ページにリダイレクトされることを検証
    '''

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )

    def test_loggedin_user_get_regist_page_redirected_to_post_index(self):
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/regist')
        self.assertRedirects(response, '/post/posts_index')


'''
user_loginページ
'''

class LoginUserLoginPageRedirectTest(TestCase):
    '''
    ログイン済みユーザーがログインページにGETリクエストすると
    投稿一覧ページにリダイレクトされることを検証
    '''

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username = 'test',
            email = 'test@email.com',
            password = 'password'
        )

    def test_loggedin_user_get_login_page_redirected_to_post_index(self):
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/user_login')
        self.assertRedirects(response, '/post/posts_index')


'''
user_editページ
'''

class NotAuthenticatedEditUderRedirectTest(TestCase):
    '''
    未認証ユーザーがユーザー編集ページにGETリクエストすると
    ログインページにリダイレクトされることを検証
    '''

    def test_not_authenticated_user_get_user_edit_page_redirected_to_login(self):
        response = self.client.get('/accounts/user_edit')
        self.assertRedirects(response, '/accounts/user_login')


'''
users_indexページ
'''

class NotAuthenticatedUserIndexRedirectTest(TestCase):
    '''
    未認証ユーザーがユーザー一覧ページにGETリクエストすると
    ログインページにリダイレクトされることを検証
    '''

    def test_not_authenticated_user_get_user_index_page_redirected_to_login(self):
        response = self.client.get('/accounts/users_index')
        self.assertRedirects(response, '/accounts/user_login')


'''
user_detailページ
'''

class NotAuthenticatedUserDetailRedirectTest(TestCase):
    '''
    未認証ユーザーがユーザー詳細ページにGETリクエストすると
    ログインページにリダイレクトされることを検証
    '''

    def test_not_authenticated_user_get_user_detail_page_redirected_to_login(self):
        response = self.client.get('/accounts/user_detail/1')
        self.assertRedirects(response, '/accounts/user_login')


'''
user_likeページ
'''

class NotAuthenticatedUserLikeRedirectTest(TestCase):
    '''
    未認証ユーザーがユーザーいいねページにGETリクエストすると
    ログインページにリダイレクトされることを検証
    '''

    def test_not_authenticated_user_get_user_like_page_redirected_to_login(self):
        response = self.client.get('/accounts/user_like/1')
        self.assertRedirects(response, '/accounts/user_login')