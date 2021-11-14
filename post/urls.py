from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('create_post', views.create_post, name='create_post'),
    path('posts_index', views.posts_index, name='posts_index'),
]