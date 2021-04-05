from django import forms
from .models import post , comment
class PostForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    content=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'type post ...'}))
    class Meta:
        model = post
        fields = ['content','image']
class CommentForm(forms.ModelForm):
    comment_content=forms.CharField(label='',widget=forms.Textarea(attrs={'rows':1}))
    comment_content=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'write comment...........'}))
    class Meta:
        model = comment
        fields = ['comment_content',]