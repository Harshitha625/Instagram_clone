from django.contrib import admin
from . models import Profile,Posts,Comments,Savedposts,Follow,Like,Notifications,Conversation,Messages

# Register your models here.
admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Savedposts)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Notifications)
admin.site.register(Conversation)
admin.site.register(Messages)