from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from .models import Posts
from django.contrib.auth.decorators import login_required


@login_required
def create_post(request):
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

@login_required
def posts_index(request):
    posts = Posts.objects.order_by('-updated_at').all()
    return render(
        request, 'post/posts_index.html', context={
            'posts': posts
        }
    )