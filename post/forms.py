from django import forms
from .models import Posts


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Posts
        fields = ('content',)