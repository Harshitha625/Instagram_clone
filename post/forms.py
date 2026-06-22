from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import Posts

class addPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('img','caption')


