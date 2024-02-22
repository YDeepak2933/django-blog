from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from autoslug import AutoSlugField
from tinymce.models import HTMLField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, default=None)
    content = HTMLField()
    image = models.ImageField(blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    def get_absolute_url(self):
        return reverse("blogs")

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    dateTime = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + " Comment: " + self.content
