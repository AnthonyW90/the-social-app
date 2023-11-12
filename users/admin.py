from django.contrib import admin
from .models import User, FriendRequest


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    readonly_fields = ("date_joined", "last_login")


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("from_friend", "to_friend", "created", "status")
    search_fields = ("from_friend__username", "to_friend__username")
    list_filter = ("status",)


admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
