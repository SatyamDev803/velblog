from django.db import models

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(blank=True)
    slug = models.SlugField(max_length=255, unique=True) 

    def __str__(self):
        return self.title + ' by ' + self.author