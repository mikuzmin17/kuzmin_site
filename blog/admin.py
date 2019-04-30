from django.contrib import admin

# Register your models here.
from blog.models import Post, Comment # наша модель из blog/models.py

admin.site.register(Post)
admin.site.register(Comment)
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'date', 'status')
#     list_filter = ('status',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'post')
#     ordering = ('-created',)