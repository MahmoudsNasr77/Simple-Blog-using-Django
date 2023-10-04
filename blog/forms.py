from django import forms
from .models import Comment,Post
class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=255)
    from_emai=forms.EmailField()
    to_email=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
 class Meta:
    model = Comment
    fields = ['name', 'email', 'body']
class PostForm(forms.ModelForm):
 class Meta:
    model = Post
    fields = ['title', 'body','user', 'status','tag']
class SearchForm(forms.Form):
    query = forms.CharField()