from django.shortcuts import render, redirect
from .models import Post, Comment


def create_post(request):
    if request.method != "POST":
        return redirect("/")
    # POST
    content = request.POST["post"]
    post = Post.objects.create(body=content, author=request.user)
    # redirect back to users profile
    return redirect("users:profile", username=request.user.username)


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author != request.user:
        return redirect("/")
    post.delete()
    return redirect("users:profile", username=request.user.username)
