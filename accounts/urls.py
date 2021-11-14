from django.urls import path
from . import views
from .views import (
    AboutView, TopView)


app_name = 'accounts'

urlpatterns = [
    path('', TopView.as_view(), name='top'),
    path('about', AboutView.as_view(), name='about'),
    path('regist', views.regist, name='regist'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_edit', views.user_edit, name='user_edit'),
]