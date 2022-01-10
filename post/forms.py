from django import forms
from .models import Posts
from django.core.exceptions import ValidationError


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Posts
        fields = ('content',)
    

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 140:
            raise ValidationError('文字数は140文字以下にしてください。')
        return content