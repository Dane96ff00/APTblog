from django.contrib import admin
from .models import Post, Comment

#register the models on the admin page
admin.site.register(Post)
admin.site.register(Comment)
