from django.shortcuts import get_object_or_404, render, redirect
from . import forms
from django.contrib import messages
from .models import Posts
from django.contrib.auth.decorators import login_required



def create_post(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        create_post_form = forms.CreatePostForm(request.POST or None)
        if create_post_form.is_valid():
            create_post_form.instance.user = request.user
            create_post_form.save()
            messages.success(request, '投稿を作成しました。')
            return redirect('post:posts_index')
        return render(
            request, 'post/create_post.html', context={
                'create_post_form': create_post_form,
            }
        )



def posts_index(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        posts = Posts.objects.order_by('-updated_at').all()
        return render(
            request, 'post/posts_index.html', context={
                'posts': posts
            }
        )


def post_detail(request, post_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        post = get_object_or_404(Posts, id=post_id)
        return render(request, 'post/post_detail.html', context={
            'post' : post
        })
