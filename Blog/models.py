from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content = RichTextUploadingField()
    image=models.ImageField(upload_to='post_images/', null=True , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField( User, related_name='saved_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        db_table='Post'


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE , related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='Comment'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.png')

    def __str__(self):
        return self.user.username


