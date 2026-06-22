from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    pfp = models.ImageField(upload_to='uploads/%Y/%m/%d')
    bio = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads/%Y/%m/%d')
    caption = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'


    def __str__(self):
        return f"{self.user.username}'s Post"