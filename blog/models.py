from django.conf import settings
from django.db import models
from django.utils import timezone


#define a Model to define a blog post with different properties (author, title, text, created_date and published_date)
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #author is the username
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

#define method
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

#define a Model to define a comment with different properties (post, author, text, created_date, approved_comment)
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)                                   #author has to be typed, in case also not registert users could comment a post (this will be audjusted in blog/views.py - add_comment_to_post)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)                       #just approved comments are visible for not registert users

#define method
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
