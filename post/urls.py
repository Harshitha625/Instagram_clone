from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('profile/<str:username>/',views.profilepage,name='profilepage'),
    path('add/',views.add_post,name='add_post'),
    path('view_post/<int:pk>/',views.view_post,name='view_post'),
    path('edit/<int:pk>/',views.edit_post,name='edit_post'),
    path('delete/<int:pk>/',views.delete_post,name='delete_post'),
]