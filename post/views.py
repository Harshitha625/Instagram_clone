from django.shortcuts import get_object_or_404, redirect,render
from . models import Posts,Profile
from django.contrib.auth.models import User
from . forms import addPostForm

def home(request):
    posts = Posts.objects.all()
    print(posts)
    context = {
        'posts' : posts,
    }
    return render(request,'home.html',context)


def profilepage(request,username):
    user = get_object_or_404(User,username = username)
    profile = get_object_or_404(Profile,user = user)
    posts = Posts.objects.filter(user = user).order_by('created_at')
    posts_count = posts.count()

    context = {
        'user':user,
        'profile':profile,
        'posts':posts,
        'posts_count' : posts_count,
    }

    return render(request,'profilepage.html',context)


def add_post(request):
    if request.method == 'POST':
        form = addPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profilepage',username = request.user.username)
    form = addPostForm()
    context = {
        'form':form,
    }
    return render(request,'add_post.html',context)

def view_post(request,pk):
    post = get_object_or_404(Posts,pk = pk)
    context = {
        'post':post,
    }
    return render(request,'single_post.html',context)

def edit_post(request,pk):
    post = get_object_or_404(Posts,pk = pk)
    if request.method == "POST":
        form = addPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_post',pk = pk)
    form = addPostForm(instance=post)
    context = {
        'form':form,
    }
    return render(request,'edit_post.html',context)


def delete_post(request,pk):
    post = get_object_or_404(Posts,pk = pk)
    post.delete()
    return redirect('profilepage',username = request.user.username)


