from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # django default user model - password = password1 and confirm password = password2
        fields = {'email','username','password1','password2'}