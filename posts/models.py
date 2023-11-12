from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("users.User", related_name="post_likes", blank=True)
    # stats
    likeCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    shareCount = models.IntegerField(default=0)
    viewCount = models.IntegerField(default=0)
    # settings
    isPrivate = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:20]

    def reply_to_post(self, author, body):
        comment = Comment.objects.create(post=self, author=author, body=body)
        return comment

    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        "users.User", related_name="comment_likes", blank=True
    )
    # stats
    likeCount = models.IntegerField(default=0)
    # settings
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:20]

    def children(self):
        return Comment.objects.filter(parent=self)

    def reply_to_comment(self, author, body):
        comment = Comment.objects.create(parent=self, author=author, body=body)
        return comment
