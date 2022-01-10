from django.db import models
from django.core.exceptions import ValidationError


class Posts(models.Model):
    content = models.CharField('ツイート内容', max_length=140)
    user = models.ForeignKey('accounts.Users', verbose_name='ユーザー',on_delete=models.CASCADE)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        db_table = 'posts'
    
    def __str__(self):
        return self.content
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 140:
            raise ValidationError('文字数は140文字以下にしてください。')
        return content


class Likes(models.Model):
    post = models.ForeignKey('post.Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'likes'