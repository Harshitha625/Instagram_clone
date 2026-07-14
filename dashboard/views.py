from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from post.models import Posts, Comments, Story



def admin_dashboard(request):
    context = {
        "users": User.objects.count(),
        "posts": Posts.objects.count(),
        "comments": Comments.objects.count(),
        "stories": Story.objects.count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


def manage_users(request):
    users = User.objects.all().order_by("-id")

    return render(request, "dashboard/manage_users.html", {
        "users": users
    })


def manage_posts(request):
    posts = Posts.objects.select_related("user").order_by("-created_at")

    return render(request, "dashboard/manage_posts.html", {
        "posts": posts
    })


def manage_comments(request):
    comments = Comments.objects.select_related("user", "post").order_by("-created_at")

    return render(request, "dashboard/manage_comments.html", {
        "comments": comments
    })


def manage_stories(request):
    stories = Story.objects.select_related("user").order_by("-created_at")

    return render(request, "dashboard/manage_stories.html", {
        "stories": stories
    })

@login_required
def delete_user(request, pk):
    if not request.user.is_superuser:
        return redirect("home")

    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        return redirect("manage_users")

    user.delete()
    return redirect("manage_users")

@login_required
def delete_post_admin(request, pk):
    if not request.user.is_superuser:
        return redirect("home")

    post = get_object_or_404(Posts, pk=pk)
    post.delete()

    return redirect("manage_posts")

@login_required
def delete_comment_admin(request, pk):
    if not request.user.is_superuser:
        return redirect("home")

    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()

    return redirect("manage_comments")

@login_required
def delete_story_admin(request, pk):
    if not request.user.is_superuser:
        return redirect("home")

    story = get_object_or_404(Story, pk=pk)
    story.delete()

    return redirect("manage_stories")


from .forms import EditUserForm

@login_required
def edit_user(request, pk):
    if not request.user.is_superuser:
        return redirect("home")

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("manage_users")

    form = EditUserForm(instance=user)
    return render(request, "dashboard/edit_user.html", {"form": form})

