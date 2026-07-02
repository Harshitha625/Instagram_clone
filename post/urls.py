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
]