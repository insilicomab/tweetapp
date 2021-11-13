from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


class TopView(TemplateView):
    template_name = 'accounts/top.html'


class AboutView(TemplateView):
    template_name = 'accounts/about.html'


def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('accounts:top')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )


def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログインしました。')
                return redirect('accounts:top')
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