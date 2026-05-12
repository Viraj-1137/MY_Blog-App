from django import forms
from Blog.models import Post , Comment , Profile
from django.forms.models import ModelForm


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control bio-input',
                'rows': 5,
                'placeholder':
                'Tell people something about yourself...'
            }),

        }
