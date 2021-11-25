from django.urls import path
from . import views
from .views import AboutView


app_name = 'accounts'

urlpatterns = [
    path('', views.top, name='top'),
    path('about', AboutView.as_view(), name='about'),
    path('accounts/regist', views.regist, name='regist'),
    path('accounts/user_login', views.user_login, name='user_login'),
    path('accounts/user_logout', views.user_logout, name='user_logout'),
    path('accounts/user_edit', views.user_edit, name='user_edit'),
    path('accounts/users_index', views.users_index, name='users_index'),
    path('accounts/user_detail/<int:user_id>', views.user_detail, name='user_detail'),
    path('accounts/user_like/<int:user_id>', views.user_like, name='user_like'),
]