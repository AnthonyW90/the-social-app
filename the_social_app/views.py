from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect("users:profile", username=request.user.username)
    return render(request, "index.html")
