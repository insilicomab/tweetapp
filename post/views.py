from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from . import forms
from django.contrib import messages
from .models import Likes, Posts
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
        likes_count = post.likes_set.all().count()
        liked = post.likes_set.filter(user=request.user)
        return render(request, 'post/post_detail.html', context={
            'post' : post,
            'likes_count' : likes_count,
            'liked': liked,
        })


def likefunc(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        if request.method =="POST":
            post = get_object_or_404(Posts, pk=request.POST.get('post_id'))
            user = request.user
            liked = False
            like = Likes.objects.filter(post=post, user=user)
            if like.exists():
                like.delete()
            else:
                like.create(post=post, user=user)
                liked = True
            
            context = {
                'post_id': post.id,
                'liked': liked,
                'likes_count': post.likes_set.all().count()
            }
        
        if request.is_ajax():
            return JsonResponse(context)

        


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        post = get_object_or_404(Posts, id=post_id)
        if post.user.id != request.user.id:
            messages.warning(request, '権限がありません')
            return redirect('post:posts_index')
        edit_post_form = forms.CreatePostForm(request.POST or None, instance=post)
        if edit_post_form.is_valid():
            edit_post_form.save()
            messages.success(request, '投稿を編集しました')
            return redirect('post:posts_index')
        return render(request, 'post/edit_post.html', context={
            'edit_post_form': edit_post_form,
            'post': post
        })


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'ログインが必要です')
        return redirect('accounts:user_login')
    else:
        post = get_object_or_404(Posts, id=post_id)
        if post.user.id != request.user.id:
            messages.warning(request, '権限がありません')
            return redirect('post:posts_index')
        post.delete()
        messages.success(request, '投稿を削除しました')
        return redirect('post:posts_index')
        