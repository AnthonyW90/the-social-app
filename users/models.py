from django.db import models
from django.contrib.auth.models import AbstractUser
from posts.models import Post, Comment


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    friends = models.ManyToManyField("self", blank=True)
    # stats
    friendCount = models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    profileViewCount = models.IntegerField(default=0)
    profileLikeCount = models.IntegerField(default=0)
    # settings
    isPrivate = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    isSuspended = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    isBanned = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def create_friend_request(self, to_friend):
        friend_request, created = FriendRequest.objects.get_or_create(
            from_friend=self, to_friend=to_friend
        )
        return friend_request

    def remove_friend(self, to_friend):
        self.friends.remove(to_friend)
        to_friend.friends.remove(self)
        return None

    def get_friends(self):
        return self.friends.all()

    def get_friend_requests(self):
        return FriendRequest.objects.filter(to_friend=self)

    def get_friend_suggestions(self):
        # get 10 random users that are not friends with self
        return (
            User.objects.filter(friends__in=self.friends.all())
            .exclude(id__in=self.friends.values_list("id", flat=True))
            .exclude(id=self.id)
            .distinct()
        )

    def get_friend_suggestions_count(self):
        return (
            User.objects.filter(friends__in=self.friends.all())
            .exclude(id__in=self.friends.values_list("id", flat=True))
            .exclude(id=self.id)
            .distinct()
            .count()
        )

    def get_friend_count(self):
        return self.friends.all().count()

    def get_friends_posts(self):
        # get posts from friends and self

        return Post.objects.filter(
            author__in=self.friends.all() | User.objects.filter(pk=self.pk)
        ).order_by("-created_at")

    def get_own_posts(self):
        return Post.objects.filter(author=self).order_by("-created_at")


REQUEST_STATUS = (
    (0, "Pending"),
    (1, "Accepted"),
    (2, "Rejected"),
    (3, "Blocked"),
)


class FriendRequest(models.Model):
    from_friend = models.ForeignKey(
        User, related_name="friend_set", on_delete=models.CASCADE
    )
    to_friend = models.ForeignKey(
        User, related_name="to_friend_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.IntegerField(choices=REQUEST_STATUS, default=0)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.from_friend} follows {self.to_friend}"

    def accept(self):
        self.status = 1
        self.save()

        # create friendship from both sides
        self.from_friend.friends.add(self.to_friend)
        self.to_friend.friends.add(self.from_friend)

        # delete any reverse requests
        FriendRequest.objects.filter(
            from_friend=self.to_friend, to_friend=self.from_friend
        ).delete()

    def reject(self):
        self.status = 2
        self.save()

    def block(self):
        self.status = 3
        self.save()
