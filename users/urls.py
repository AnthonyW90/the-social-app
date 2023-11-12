from django.urls import path

from .views import signup_page, login_page, logout_page, profile_page, add_friend

app_name = "users"

urlpatterns = [
    path("signup/", signup_page, name="signup"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("<str:username>/", profile_page, name="profile"),
    path("friend/<int:pk>/", add_friend, name="add_friend"),
]
