from django.shortcuts import get_object_or_404, redirect,render
from . models import Posts,Profile,Comments,Like,Follow,Savedposts,Notifications,Story,Conversation,Messages
from django.contrib.auth.models import User
from . forms import addPostForm,ChangeProfile,CommentForm,StoryForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import Random

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
            if request.user != post.user:
                Notifications.objects.create(
                    sender = request.user,
                    receiver = post.user,
                    notification_type = "comment",
                    post = post,
                )
            return redirect('home')
    comment_form = CommentForm()

    following_users = Follow.objects.filter(follower = request.user)
    users = [follow.following for follow in following_users]
    # if no posts of following users then see your posts in the feed
    users.append(request.user)
    posts = Posts.objects.filter(user__in = users).order_by('-created_at')

    #To making liked posts red color
    #To making saved posts white color
    for post in posts:
        post.liked = Like.objects.filter(user = request.user,post = post).exists()
        post.saved = Savedposts.objects.filter(user = request.user,post = post).exists()
    
    ####################   Suggestions feed ##########################
    following_users = Follow.objects.filter(follower = request.user)
    following_ids = following_users.values_list("following_id",flat=True)
    # exclude the following you follow and exclude you
    suggestions = User.objects.exclude(
        id__in = following_ids
    ).exclude(
        id = request.user.id
    )
    suggestions = suggestions.order_by(Random())[:5]
    ### ends here ###

    # -----stories----- #
    time_limit = timezone.now()-timedelta(hours=24)
    stories = Story.objects.filter(
        created_at__gte = time_limit
    ).order_by('-created_at')
    users_seen = set()
    story_users = []
    for story in stories:
        if story.user.id not in users_seen:
            users_seen.add(story.user.id)
            story_users.append(story)

    context = {
        'posts' : posts,
        'comment_form':comment_form,
        'suggestions':suggestions,
        'stories' : story_users,
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
            if request.user != post.user:
                Notifications.objects.create(
                    sender = request.user,
                    receiver = post.user,
                    notification_type = "comment",
                    post = post,
                )
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
    post = get_object_or_404(Posts,pk = pk,user = request.user)
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
    post = get_object_or_404(Posts,pk = pk,user = request.user)
    post.delete()
    return redirect('profilepage',username = request.user.username)


@login_required
def editProfile(request,username):
    if(request.user.username != username):
        return redirect('home')
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
    post = comment.post
    user = post.user
    # user can delete their comment and post user can delete the comment
    if comment.user == request.user or request.user == post.user:
        comment.delete()
        # after deleting the notification must be deleted from the post user
        if request.user != post.user:
            Notifications.objects.filter(
                sender = comment.user,
                receiver = user,
                post = post,
                notification_type = 'comment'
            ).delete()
    return redirect(request.META.get("HTTP_REFERER","home"))


@login_required
def like_post(request,pk):
    post = get_object_or_404(Posts,pk=pk)
    like = Like.objects.filter(user = request.user,post = post)
    if like.exists():
        like.delete() #unlike
        Notifications.objects.filter(
                sender = request.user ,receiver = post.user,notification_type = "like",post = post
            ).delete()
    else:
        Like.objects.create(user = request.user,post = post)
        if request.user != post.user:
            Notifications.objects.create(
                sender = request.user ,receiver = post.user,notification_type = "like",post = post
            )
    return redirect(request.META.get("HTTP_REFERER","home"))

@login_required
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
        Notifications.objects.filter(
            sender = request.user,
            receiver = user_to_follow,
            notification_type = "follow"
        ).delete()
    else:
        Follow.objects.create(
            follower = request.user,
            following = user_to_follow
        )
        Notifications.objects.create(
            sender = request.user,
            receiver = user_to_follow,
            notification_type = "follow"
        )
    return redirect('profilepage',username = username)



# show followers list
@login_required
def view_followers(request,username):
    user = get_object_or_404(User,username = username)
    followers = Follow.objects.filter(following = user)
    context = {
        'followers':followers,
    }
    return render(request,'view_followers.html',context)

# show following list
@login_required
def view_following(request,username):
    user = get_object_or_404(User,username = username)
    following = Follow.objects.filter(follower = user)
    context = {
        'following':following,
    }
    return render(request,'view_following.html',context)

@login_required
def search_user(request):
    keyword = request.GET.get('q')
    users = None
    if keyword:
        # exclude the requested user
        users = User.objects.filter(username__icontains = keyword).exclude(id=request.user.id)
    context = {
        'users':users,
        'keyword':keyword,
    }
    return render(request,'search_user.html',context)


@login_required
def save_post(request,pk):
    post = get_object_or_404(Posts,pk = pk)
    user = request.user
    save_post = Savedposts.objects.filter(
        user = user,
        post = post
    )
    if save_post.exists():
        save_post.delete()
    else:
        Savedposts.objects.create(
            user = user,
            post = post
        )
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def saved_posts(request):
    user = request.user
    saved_posts = Savedposts.objects.filter(user = user)

    context = {
        'saved_posts':saved_posts,
    }
    return render(request,'saved_posts.html',context)

@login_required
def view_notifications(request):
    notifications = Notifications.objects.filter(receiver= request.user).order_by('-created_at')
    notifications.update(is_read = True)
    context = {
        'notifications':notifications,
    }
    return render(request,'notifications.html',context)

    

@login_required
def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST,request.FILES)

        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect("home")
    else:
        form = StoryForm()

    context = {
        'form':form,
    }
    return render(request,'add_story.html',context)

@login_required
def view_story(request,username):
    user = get_object_or_404(User,username = username)
    time_limit = timezone.now() - timedelta(hours = 24)
    stories = Story.objects.filter(user = user,
        created_at__gte = time_limit).order_by("-created_at")
    context = {
        'stories':stories,
        'story_user':user,
    }
    return render(request, "view_story.html", context)

@login_required
def delete_story(request,pk):
    story = get_object_or_404(Story,pk = pk)
    story.delete()
    return redirect('home')

@login_required
def inbox(request):
    if request.method == "GET":
        keyword = request.GET.get('q')
        users = None
        if keyword:
            users = User.objects.filter(username__icontains = keyword).exclude(id=request.user.id)
    conversations = Conversation.objects.filter(
        participants= request.user
    ).order_by("-created_at")
    context = {
        'conversations':conversations,
        'search_users':users,
    }
    return render(request,'inbox.html',context)

@login_required
def start_chat(request,username):
    other_user = get_object_or_404(User,username = username)
    conversation = Conversation.objects.filter(
        participants = request.user
    ).filter(
        participants = other_user
    ).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user,other_user)

    return redirect("chat",conversation.id)


@login_required
def chat(request,conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id = conversation_id,
        participants = request.user,
    )
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Messages.objects.create(
                conversation = conversation,
                sender = request.user,
                text = text,
            )
            return redirect("chat",conversation_id = conversation_id)
    messages = Messages.objects.filter(
        conversation = conversation,
    ).order_by("created_at")
    context = {
        "conversation": conversation,
        "messages": messages,
    }
    return render(request,'chat.html',context)
