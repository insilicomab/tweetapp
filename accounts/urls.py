from django.urls import path
from . import views
from .views import (
    AboutView, TopView)


app_name = 'accounts'

urlpatterns = [
    path('', views.top, name='top'),
    path('about', AboutView.as_view(), name='about'),
    path('regist', views.regist, name='regist'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('users_index', views.users_index, name='users_index'),
    path('user_detail/<int:user_id>', views.user_detail, name='user_detail'),
]