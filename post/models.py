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
    img = models.ImageField(upload_to='uploads/%Y/%m/%d',blank=True,null=True)
    video = models.FileField(upload_to='uploads/%Y/%m/%d',blank=True,null=True)
    caption = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'


    def __str__(self):
        return f"{self.user.username}'s Post"
    

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE )
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"{self.user.username}:{self.text[:30]}"
    


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','post') #single like by a single user


class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("follower","following")

    def __str__(self):
        return f'{self.follower.username} "follows" {self.following.username}'
    
    
