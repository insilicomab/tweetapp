from django.db import models


class Posts(models.Model):
    content = models.CharField('ツイート内容', max_length=140)
    user = models.ForeignKey('accounts.Users', verbose_name='ユーザー',on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        db_table = 'posts'
    
    def __str__(self):
        return self.content


class Likes(models.Model):
    post = models.ForeignKey('post.Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'likes'