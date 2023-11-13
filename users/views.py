from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def signup_page(request):
    if request.method != "POST":
        return render(request, "users/signup.html")

    # POST
    username = request.POST["username"]
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return render(
            request, "users/signup.html", {"error": "Username already exists"}
        )

    password = request.POST["password"]
    password2 = request.POST["passwordConfirm"]
    if password != password2:
        return render(request, "users/signup.html", {"error": "Passwords don't match"})

    email = request.POST["email"]
    first_name = request.POST["firstName"]
    last_name = request.POST["lastName"]

    # Create user
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    login(request, user)
    return redirect("index")


def login_page(request):
    if request.method != "POST":
        return render(request, "users/login.html")

    # POST
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "users/login.html", {"error": "Invalid credentials"})

    login(request, user)
    return redirect("index")


def logout_page(request):
    logout(request)
    return render(request, "users/login.html", {"messages": ["Logged out!"]})


def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    suggestions = request.user.get_friend_suggestions()[:5]
    context = {
        "user": user,
        "suggestions": suggestions,
    }
    if user == request.user:
        posts = user.get_friends_posts()
        context["posts"] = posts
        context["is_owner"] = True
    else:
        user.profileViewCount += 1
        user.save()
        context["is_owner"] = False
        context["posts"] = user.get_own_posts()

    return render(request, "users/profile.html", context)


def add_friend(request, pk):
    user = get_object_or_404(User, pk=pk)
    request.user.friends.add(user)
    return redirect("users:profile", username=user.username)
