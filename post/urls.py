from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('profile/<str:username>/',views.profilepage,name='profilepage'),
    # posts crud
    path('add/',views.add_post,name='add_post'),
    path('view_post/<int:pk>/',views.view_post,name='view_post'),
    path('edit/<int:pk>/',views.edit_post,name='edit_post'),
    path('delete/<int:pk>/',views.delete_post,name='delete_post'),
    path('editProfile/<str:username>/',views.editProfile,name='editProfile'),

    # delete comment
    path('delele_comment/<int:pk>/',views.delete_comment,name='delete_comment'),
    # like post
    path('like_post/<int:pk>/',views.like_post,name='like_post'),
    # follow 
    path('follow/<str:username>/',views.follow_user,name='follow_user'),
    # show followers & following
    path('followers/<str:username>/',views.view_followers,name='view_followers'),
    path('following/<str:username>/',views.view_following,name='view_following'),
    # search users
    path('search/',views.search_user,name='search_user'),
    # save posts
    path('save/<int:pk>',views.save_post,name='save'),
    # show saved posts
    path('saved_posts/',views.saved_posts,name='saved_posts'),
    # show notifications
    path('view_notifications/',views.view_notifications,name = 'view_notifications'),
    # add the story
    path('story/add/',views.add_story,name = 'add_story'),
    path('stories/<str:username>/',views.view_story,name = 'view_story'),
]