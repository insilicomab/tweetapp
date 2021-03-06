from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from post.models import Likes, Posts
from . import forms
from .models import Users


def top(request):
    if request.user.is_authenticated:
        messages.warning(request, 'すでにログインしています')
        return redirect('post:posts_index')
    return render(request, 'accounts/top.html')


class AboutView(TemplateView):
    template_name = 'accounts/about.html'


def regist(request):
    if request.user.is_authenticated:
        messages.warning(request, 'すでにログインしています')
        return redirect('post:posts_index')
    else:
        regist_form = forms.RegistForm(request.POST or None)
        if regist_form.is_valid():
            try:
                regist_form.save()
                email = regist_form.cleaned_data.get('email')
                password = regist_form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                login(request, user)
                messages.success(request, 'ユーザー登録が完了しました')
                return redirect('post:posts_index')
            except ValidationError as e:
                regist_form.add_error('password', e)
        return render(
            request, 'accounts/regist.html', context={
                'regist_form': regist_form,
            }
        )


def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'すでにログインしています')
        return redirect('post:posts_index')
    else:
        login_form = forms.LoginForm(request.POST or None)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'ログインしました')
                    return redirect('post:posts_index')
                else:
                    return render(
                    request, 'accounts/user_login.html', {
                        'error_message' : 'ユーザがアクティブでありません',
                        'login_form': login_form,
                    }
                )
            else:
                return render(
                    request, 'accounts/user_login.html', {
                        'error_message' : 'メールアドレスまたはパスワードが間違っています',
                        'login_form': login_form,
                    }
                )
        return render(
            request, 'accounts/user_login.html', context={
                'login_form': login_form,
            }
        )


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:user_login')


def user_edit(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
        if user_edit_form.is_valid():
            messages.success(request, 'ユーザー情報を編集しました')
            user_edit_form.save()
            return redirect('post:posts_index')
        return render(request, 'accounts/user_edit.html', context={
            'user_edit_form': user_edit_form,
        })


def users_index(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        users = Users.objects.order_by('-id').all()
        return render(request, 'accounts/users_index.html', context={
            'users': users
        })


def user_detail(request, user_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        user = get_object_or_404(Users, id=user_id)
        posts = Posts.objects.filter(
            user_id=user_id).order_by('-created_at')
        return render(request, 'accounts/user_detail.html', context={
            'user': user, 'posts' : posts
        })


def user_like(request, user_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        user = get_object_or_404(Users, id=user_id)
        likes = Likes.objects.filter(
            user_id=user.id).order_by('-created_at')
        return render(request, 'accounts/user_like.html', context={
            'user': user, 'likes': likes
        })