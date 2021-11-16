from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('create_post', views.create_post, name='create_post'),
    path('posts_index', views.posts_index, name='posts_index'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
]