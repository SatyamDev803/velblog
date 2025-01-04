from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# from tinymce.models import HTMLField

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    # content = HTMLField()
    content = models.TextField()
    author = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(default=now, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.sno} - {self.title} by {self.author}"


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"