# -*- coding: utf-8 -*-

from django.contrib import admin
# Register your models here.
from blog.models import Post, Comment, UserAccount


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserAccount)
