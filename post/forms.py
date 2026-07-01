from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import Posts,Profile,Comments

class addPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('img','video','caption')


class ChangeProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','pfp','bio')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']