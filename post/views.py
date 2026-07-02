from django.shortcuts import get_object_or_404, redirect,render
from . models import Posts,Profile,Comments,Like,Follow
from django.contrib.auth.models import User
from . forms import addPostForm,ChangeProfile,CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.user = request.user
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Posts,pk = post_id)
            comment.post = post

            # check if there is a reply
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent = get_object_or_404(Comments,pk = parent_id)
                comment.parent = parent
            comment.save()
            return redirect('home')
    comment_form = CommentForm()
    posts = Posts.objects.all()

    # making liked posts red color
    for post in posts:
        post.liked = Like.objects.filter(user = request.user,post = post).exists()
    context = {
        'posts' : posts,
        'comment_form':comment_form,
    }
    return render(request,'home.html',context)


@login_required
def profilepage(request,username):
    user = get_object_or_404(User,username = username)
    profile = get_object_or_404(Profile,user = user)
    posts = Posts.objects.filter(user = user).order_by('-created_at')
    posts_count = posts.count()

    is_following = False
    if request.user !=user:
        is_following = Follow.objects.filter(
            follower = request.user,
            following = user
        ).exists()

    following_count = user.following.count()
    followers_count = user.followers.count()

    context = {
        'user':user,
        'profile':profile,
        'posts':posts,
        'posts_count' : posts_count,
        'is_following': is_following,
        'following_count':following_count,
        'follower_count':followers_count,
    }

    return render(request,'profilepage.html',context)


@login_required
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

@login_required
def view_post(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post

            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent = get_object_or_404(Comments, pk=parent_id)

            comment.save()
            return redirect("view_post", pk=pk)
        
    post.liked = Like.objects.filter(post=post,user=request.user).exists()
    comment_form = CommentForm()
    context = {
        "post": post,
        "comment_form": comment_form,
    }

    return render(request, "single_post.html", context)

@login_required
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

@login_required
def delete_post(request,pk):
    post = get_object_or_404(Posts,pk = pk)
    post.delete()
    return redirect('profilepage',username = request.user.username)

@login_required
def editProfile(request,username):
    user = get_object_or_404(User,username = username)
    profile = user.profile
    if request.method == 'POST':
        form = ChangeProfile(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profilepage',username)
    form = ChangeProfile(instance=profile)
    context = {
        'form':form,
    }
    return render(request,'editprofile.html',context)



@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comments,pk=pk)
    
    if comment.user == request.user:
        comment.delete()
    return redirect(request.META.get("HTTP_REFERER","home"))


@login_required
def like_post(request,pk):
    post = get_object_or_404(Posts,pk=pk)
    like = Like.objects.filter(user = request.user,post = post)
    if like.exists():
        like.delete() #unlike
    else:
        Like.objects.create(user = request.user,post = post)

    return redirect(request.META.get("HTTP_REFERER","home"))


def follow_user(request,username):
    user_to_follow = get_object_or_404(User,username = username)
    # prevent follow urself
    if request.user == user_to_follow:
        return redirect('profilepage',username = username)
    
    follow = Follow.objects.filter(
        follower = request.user,
        following = user_to_follow
    )
    if follow.exists():
        follow.delete()
    else:
        Follow.objects.create(
            follower = request.user,
            following = user_to_follow
        )
    return redirect('profilepage',username = username)