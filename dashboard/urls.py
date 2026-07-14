from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),

    path("users/", views.manage_users, name="manage_users"),
    path("posts/", views.manage_posts, name="manage_posts"),
    path("comments/", views.manage_comments, name="manage_comments"),
    path("stories/", views.manage_stories, name="manage_stories"),

    path("dashboard/delete-user/<int:pk>/", views.delete_user, name="delete_user"), 
    path("dashboard/delete-post/<int:pk>/", views.delete_post_admin, name="delete_post_admin"),
    path("dashboard/delete-comment/<int:pk>/", views.delete_comment_admin, name="delete_comment_admin"),
    path("dashboard/delete-story/<int:pk>/", views.delete_story_admin, name="delete_story_admin"),

    path("dashboard/edit-user/<int:pk>/", views.edit_user, name="edit_user"),
]
