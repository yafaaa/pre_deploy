from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Comment


def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        content = request.POST.get("content")
        if content:
            Post.objects.create(user=request.user, content=content)
            
    # Get all posts and order by timestamp (newest first)
    posts_list = Post.objects.all().order_by("-timestamp")
    
    # Set up pagination - 10 posts per page
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)  # 10 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/all_posts.html", {
        "posts": posts
    })


@login_required
def following(request):
    following_users = request.user.following.all()
    posts_list = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": posts
    })


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(user=profile_user).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    is_following = request.user in profile_user.followers.all()
    can_follow = request.user != profile_user

    if request.method == "POST" and can_follow:
        if is_following:
            profile_user.followers.remove(request.user)
        else:
            profile_user.followers.add(request.user)
        return redirect('profile', username=username)

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "is_following": is_following,
        "can_follow": can_follow,
    }
    return render(request, "network/profile.html", context)


@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if post.user != request.user:
        return JsonResponse({"error": "Not authorized."}, status=403)
    data = json.loads(request.body)
    content = data.get("content", "")
    if not content:
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    post.content = content
    post.save()
    return JsonResponse({"message": "Post updated successfully."})


@login_required
@csrf_exempt
def toggle_like(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({"liked": liked, "like_count": post.likes.count()})


@login_required
@csrf_exempt
def add_comment(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # get comment content from request
    data = json.loads(request.body)
    content = data.get("content", "")
    
    if not content:
        return JsonResponse({"error": "Comment cannot be empty."}, status=400)
    
    # create comment
    comment = Comment.objects.create(
        user=request.user,
        post=post,
        content=content
    )
    
    return JsonResponse({
        "message": "Comment added successfully.",
        "comment": {
            "id": comment.id,
            "username": comment.user.username,
            "content": comment.content,
            "timestamp": comment.timestamp.strftime("%B %d, %Y, %I:%M %p")
        }
    })

def get_comments(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    comments = post.comments.all()
    comments_data = []
    
    for comment in comments:
        comments_data.append({
            "id": comment.id,
            "username": comment.user.username,
            "content": comment.content,
            "timestamp": comment.timestamp.strftime("%B %d, %Y, %I:%M %p")
        })
    
    return JsonResponse({"comments": comments_data})